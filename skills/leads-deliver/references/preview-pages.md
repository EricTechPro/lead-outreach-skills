# Preview artifacts (build before the send gate)

Every delivery run, **before sending**, `leads-deliver` builds three artifacts into
`lead-system/<campaign>/outbox/` so the user sees exactly what will go out. They are produced by
`scripts/build_previews.py` from the approved ✅ emails. The send gate shows them; nothing sends until
the user says go.

## The three files

| File | What it is | Audience |
|---|---|---|
| `_send-preview.md` | Every exact email as text — index · To · Subject · body (with `**bold**` / `==highlight==` markers visible). | The reviewer scanning quickly. |
| `_preview.html` | Every email rendered **exactly as it sends** — system font, bullets, bold, the one highlight. No card/wrapper. | The send gate (open in a browser to eyeball typography). **Private** — contains real emails + WhatsApp/WeChat. |
| `_preview-redacted.html` | Same as `_preview.html` but with recipient email, WhatsApp, and WeChat **removed** (blacked out). The YouTube link stays visible. | Shareable publicly (screenshots, posts). |
| `_send.json` *(bonus)* | `[{to, subject, html}]` — the exact HTML body each send passes verbatim, so **what was previewed is what sends**. | The send loop. |

## Redaction contract (the redacted file)
- Removes the **actual characters** of: every recipient email, the WhatsApp number, the WeChat ID —
  replaced with a blackout bar. The real values must **not** appear anywhere in the HTML source
  (not merely visually covered). `build_previews.py` verifies this and **fails** if any value leaks.
- **Keeps** the YouTube channel link visible — it's public and is the one allowed link.

## Running it

```bash
# primary — the skill writes _emails.json ([{name,email,subject,body,lang}]) + _style.json from campaign.md
python3 scripts/build_previews.py \
  --emails  lead-system/<campaign>/outbox/_emails.json \
  --config  lead-system/<campaign>/outbox/_style.json \
  --out     lead-system/<campaign>/outbox/

# fallback — parse the ✅ sections of leads-spec.md, join emails from the CSV by name
python3 scripts/build_previews.py \
  --spec lead-system/<campaign>/leads-spec.md \
  --csv  lead-system/<campaign>/leads.csv \
  --config lead-system/<campaign>/outbox/_style.json \
  --out  lead-system/<campaign>/outbox/
```

**`_style.json`** mirrors campaign.md's Delivery style — the script reads these keys (all optional;
personal values default to empty so nothing personal is baked into the repo):

```json
{
  "channel_url": "https://www.youtube.com/@erictechpro",
  "channel_handle": "youtube.com/@erictechpro",
  "whatsapp": "+1 555-867-5309",
  "wechat": "your_wechat_id",
  "highlight_hex": "#fde047"
}
```

> Whatever the renderer puts in `_preview.html` is byte-for-byte what `_send.json` hands the send node,
> so the send step never drifts from the approved preview. Body format rules: `references/email-style.md`.
> Input note: a "Name | email" line is split on the **last** `|` (display names can contain `|`).
