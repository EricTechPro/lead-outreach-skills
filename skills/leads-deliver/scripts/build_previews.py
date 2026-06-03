#!/usr/bin/env python3
"""Build the three delivery preview artifacts for a leads-deliver run.

Given the approved ✅ emails, render every message EXACTLY as it will send and emit:

  _send-preview.md       every email as text: index · To · Subject · body (markers visible)
  _preview.html          every email rendered as it sends (full / private — for the send gate)
  _preview-redacted.html  same, with recipient email + WhatsApp + WeChat blacked out (shareable)
  _send.json             [{to, subject, html}] — the exact HTML body the send step passes verbatim

The email body is plain & personal (system font, 15px/1.6, #222) with NO card/table wrapper, NO accent
rule, NO image — see references/email-style.md. The author writes the body in plain text with markers
(`- ` bullets, `**bold**`, `==highlight==`, signature lines); this script converts them to HTML so an
HTML send node (n8n "Send a message in Gmail", a make.com/Zapier webhook, a Gmail MCP, etc.) renders
bullets/bold/the single highlight instead of collapsing the newlines.

Input (pick one):
  --emails emails.json   primary: a JSON list of {name, email, subject, body[, lang]}
  --spec leads-spec.md   fallback: parse the ✅ sections (join emails from --csv by name if given)

Contact values (for the signature link + redaction) come from --config (the skill fills them from
campaign.md's Delivery style). Nothing personal is hardcoded here — defaults redact nothing.

Usage:
  build_previews.py --emails outbox/_emails.json --out outbox/ --config outbox/_style.json
  build_previews.py --spec leads-spec.md --csv leads.csv --out outbox/ --config outbox/_style.json
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

# ------------------------------------------------------------------ config defaults
# Personal contact values are NOT baked in (keeps the committed repo portable). The skill passes them
# via --config from campaign.md's Delivery style. Empty whatsapp/wechat => those values aren't redacted.
DEFAULTS = {
    "channel_url": "https://www.youtube.com/@erictechpro",  # public handle — safe default
    "channel_handle": "youtube.com/@erictechpro",           # bare display form used in the signature
    "whatsapp": "",                                          # e.g. "+1 555-867-5309"  (redacted if set)
    "wechat": "",                                            # e.g. "your_wechat_id"   (redacted if set)
    "highlight_hex": "#fde047",
}

BODY_DIV_STYLE = ("font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,"
                  "sans-serif;font-size:15px;line-height:1.6;color:#222;")


def split_name_email(s):
    """Split a "Name | email" line on the LAST '|' — display names can contain '|'
    (e.g. "Brad | AI & Automation | brad@x.com"). Returns (name, email)."""
    if "|" in s:
        name, email = s.rsplit("|", 1)
        return name.strip(), email.strip()
    return s.strip(), ""


# ------------------------------------------------------------------ inline + block rendering
def _linkify(escaped_text, cfg):
    """Wrap the (already HTML-escaped) channel link — the ONLY link allowed — in an <a>.
    Matches the full URL or the bare handle in one pass (longest alternative first => no double-wrap)."""
    href = cfg["channel_url"]
    handle = cfg["channel_handle"]
    variants = []
    if href:
        variants.append(re.escape(html.escape(href)))
    if handle:
        # bare handle not preceded by a URL char (so it won't re-match inside the full URL)
        variants.append(r"(?<![\w@/.:])" + re.escape(html.escape(handle)))
    if not variants:
        return escaped_text
    pattern = re.compile("|".join(variants))

    def repl(m):
        shown = m.group(0)
        return f'<a href="{html.escape(href)}" style="color:#1a0dab;">{shown}</a>'

    return pattern.sub(repl, escaped_text)


def _inline(text, cfg):
    """Escape one line, then linkify the channel, then **bold** and ==highlight==."""
    out = html.escape(text)
    out = _linkify(out, cfg)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    mark = f'background:{cfg["highlight_hex"]};padding:0 2px;border-radius:2px;'
    out = re.sub(r"==(.+?)==", lambda m: f'<mark style="{mark}">{m.group(1)}</mark>', out)
    return out


def render_body(body, cfg):
    """Turn the plain-text+markers body into the HTML that actually sends.

    blank line  -> paragraph break        single newline inside a block -> <br>
    `- ` lines  -> <ul><li>…</li></ul>     indented continuation line    -> joined into the prior <li>
    """
    out, para, items = [], [], []

    def flush_para():
        if para:
            out.append('<p style="margin:0 0 14px;">' + "<br>".join(_inline(x, cfg) for x in para) + "</p>")
            para.clear()

    def flush_list():
        if items:
            lis = "".join(f'<li style="margin:0 0 6px;">{_inline(x, cfg)}</li>' for x in items)
            out.append(f'<ul style="margin:0 0 14px;padding-left:22px;">{lis}</ul>')
            items.clear()

    for raw in body.split("\n"):
        if raw.strip() == "":            # blank line ends the current block
            flush_list(); flush_para()
            continue
        is_bullet = raw.lstrip().startswith(("- ", "• "))
        is_indent = raw[:1] in (" ", "\t")
        if is_bullet:
            flush_para()
            items.append(raw.lstrip()[2:].strip())
        elif items and is_indent:        # wrapped continuation of the previous bullet
            items[-1] += " " + raw.strip()
        else:
            flush_list()
            para.append(raw.strip())
    flush_list(); flush_para()
    return "\n".join(out)


def email_html(rec, cfg):
    """The exact <div> body that sends (identical in the full preview and the send step)."""
    return f'<div style="{BODY_DIV_STYLE}">\n{render_body(rec["body"], cfg)}\n</div>'


# ------------------------------------------------------------------ redaction
REDBAR = '<span style="background:#111;color:#111;border-radius:3px;">••••••</span>'


def redact(page_html, emails, cfg):
    """Remove the actual characters of every recipient email + WhatsApp + WeChat (replace with a
    blackout bar). The raw values must NOT survive anywhere in the output — verified by the caller."""
    targets = set(e for e in emails if e)
    for key in ("whatsapp", "wechat"):
        if cfg.get(key):
            targets.add(cfg[key])
    if cfg.get("whatsapp"):
        targets.add(re.sub(r"\D", "", cfg["whatsapp"]))  # also the digits-only form of the phone
    out = page_html
    for t in sorted(targets, key=len, reverse=True):     # longest first => no partial leftovers
        if not t:
            continue
        out = out.replace(t, REDBAR)
        out = out.replace(html.escape(t), REDBAR)
    return out, targets


# ------------------------------------------------------------------ page assembly
def label_block(idx, rec):
    to = html.escape(rec.get("email") or "—")
    subj = html.escape(rec.get("subject") or "—")
    name = html.escape(rec.get("name") or "—")
    return (f'<div style="font:12px ui-monospace,Menlo,monospace;color:#666;margin:0 0 8px;">'
            f'#{idx} · <b>To:</b> {name} &lt;{to}&gt; · <b>Subject:</b> {subj}</div>')


def build_html_page(records, cfg, title):
    blocks = []
    for i, rec in enumerate(records, 1):
        blocks.append(
            '<section style="max-width:680px;margin:0 auto 14px;">'
            + label_block(i, rec)
            + email_html(rec, cfg)
            + '</section>'
            + '<hr style="border:none;border-top:1px solid #e5e7eb;max-width:680px;margin:18px auto;">'
        )
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<title>{html.escape(title)}</title></head>'
            f'<body style="background:#fafafa;margin:0;padding:24px 12px;">'
            f'<p style="max-width:680px;margin:0 auto 18px;font:13px sans-serif;color:#888;">'
            f'{html.escape(title)} — {len(records)} email(s). Each block below renders exactly as it '
            f'sends (the grey line is preview-only).</p>'
            + "\n".join(blocks)
            + '</body></html>')


def build_send_preview_md(records):
    lines = [f"# Send preview — {len(records)} email(s)\n",
             "Every exact email below. `**bold**` and `==highlight==` are the emphasis markers the "
             "build step renders.\n"]
    for i, rec in enumerate(records, 1):
        lines.append(f"\n## {i} · {rec.get('name','—')}")
        lines.append(f"- **To:** {rec.get('email') or '—'}")
        lines.append(f"- **Subject:** {rec.get('subject') or '—'}\n")
        lines.append(rec["body"].rstrip())
        lines.append("\n---")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ inputs
def load_emails_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    recs = []
    for r in data:
        name, email = r.get("name", ""), r.get("email", "")
        if not email and "|" in name:        # tolerate a combined "Name | email" name field
            name, email = split_name_email(name)
        recs.append({"name": name, "email": email,
                     "subject": r.get("subject", ""), "body": r.get("body", ""),
                     "lang": r.get("lang", "")})
    return recs


def load_from_spec(spec_path, csv_path=None):
    """Fallback: parse the ✅ sections of leads-spec.md. Emails aren't in the spec, so join them from
    the CSV by name when --csv is given (else To: is blank and only the body previews)."""
    text = Path(spec_path).read_text(encoding="utf-8")
    name_to_email = {}
    if csv_path:
        import csv
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                low = {k.lower().strip(): (v or "").strip() for k, v in row.items()}
                if low.get("name") and low.get("email"):
                    name_to_email[low["name"].lower()] = low["email"]

    recs = []
    # split into ### sections; keep only ✅ ones
    sections = re.split(r"^###\s+", text, flags=re.M)
    for sec in sections:
        if not sec.startswith("✅"):
            continue
        head = sec.splitlines()[0]
        name = re.sub(r"^✅\s*", "", head).split(" — ")[0].split(" – ")[0].strip()
        subj_m = re.search(r"\*\*Subject:\*\*\s*(.+)", sec)
        subject = subj_m.group(1).strip() if subj_m else ""
        body = ""
        if subj_m:
            after = sec[subj_m.end():]
            after = re.split(r"\n---", after)[0]            # stop at the section divider
            body = after.strip("\n")
        recs.append({"name": name, "email": name_to_email.get(name.lower(), ""),
                     "subject": subject, "body": body, "lang": ""})
    return recs


# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Build leads-deliver preview artifacts.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--emails", help="JSON list of {name,email,subject,body[,lang]}")
    src.add_argument("--spec", help="leads-spec.md to parse the ✅ sections from")
    ap.add_argument("--csv", help="leads.csv to join emails by name (with --spec)")
    ap.add_argument("--config", help="JSON of Delivery-style values (channel_url, channel_handle, "
                                     "whatsapp, wechat, highlight_hex)")
    ap.add_argument("--out", default=".", help="output directory (e.g. outbox/)")
    args = ap.parse_args(argv)

    cfg = dict(DEFAULTS)
    if args.config:
        cfg.update({k: v for k, v in json.loads(Path(args.config).read_text(encoding="utf-8")).items()
                    if v is not None})

    records = load_emails_json(args.emails) if args.emails else load_from_spec(args.spec, args.csv)
    if not records:
        sys.exit("No ✅ emails found to preview.")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    emails = [r["email"] for r in records if r.get("email")]

    # 1 · text preview
    (out / "_send-preview.md").write_text(build_send_preview_md(records), encoding="utf-8")

    # 2 · full HTML preview (private)
    full = build_html_page(records, cfg, "Outreach preview (private)")
    (out / "_preview.html").write_text(full, encoding="utf-8")

    # 3 · redacted HTML preview (shareable) — keep the YouTube link, blackout email/WhatsApp/WeChat
    redacted, targets = redact(full, emails, cfg)
    # verify the raw values are GONE (the requirement: removed, not just visually covered)
    leaked = [t for t in targets if t and (t in redacted or html.escape(t) in redacted)]
    if leaked:
        sys.exit(f"Redaction failed — these values still appear: {leaked}")
    (out / "_preview-redacted.html").write_text(redacted, encoding="utf-8")

    # bonus · the exact HTML bodies the send step passes verbatim (preview == sent)
    send = [{"to": r["email"], "subject": r["subject"], "html": email_html(r, cfg)} for r in records]
    (out / "_send.json").write_text(json.dumps(send, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✓ {len(records)} email(s) → {out}/_send-preview.md, _preview.html, "
          f"_preview-redacted.html, _send.json")
    if not (cfg.get("whatsapp") or cfg.get("wechat")):
        print("  note: no whatsapp/wechat in --config, so only recipient emails were redacted.")


if __name__ == "__main__":
    main()
