---
name: leads-deliver
description: Deliver the approved outreach from leads-spec.md — select only ✅ (recommend) leads, build the three previews, show the count + the first 2 full emails for an explicit go, then send one personalized email per recipient via the user's chosen transport (n8n "Send a message in Gmail" node, a make.com/Zapier/custom webhook, a Gmail MCP, the Gmail API, or an /outbox folder if nothing is connected). Use when the user has reviewed leads-spec.md and wants to send. Also /leads-deliver. NOT for researching leads (use leads-research) and NOT for defining the campaign (use leads-plan). Sending real email is irreversible — always confirm count + sample before sending, never auto-blast.
---

# Leads — Deliver

The outbox. Turns the approved `leads-spec.md` into sent (or draft) personalized email. The spec is
the gate: the user reviewed and edited it, so this skill executes that approval — but because real
email is irreversible, it always builds a preview and confirms the count + a sample before sending.

## When to use
- "Send the approved outreach" / "deliver the leads"
- `/leads-deliver ./lead-system/<campaign>/leads-spec.md`

## When NOT to use
- The spec isn't reviewed yet → finish `leads-research` and let the user approve first.

## Inputs
- An **approved `leads-spec.md`** (from `leads-research`, edited by the user).
- The campaign's **Delivery style** (in `campaign.md`) — the contact + subject-prefix values that fill
  the template. Ask only for what's missing.

## Step 1 — Resolve the campaign style (one canonical template)
Read `references/email-style.md` and `references/email-templates.md`. This campaign type has **one
house style** — a plain, personal, creator-to-creator note sent as HTML (v3 peer networking). There is
**no template picker**; every ✅ email uses the same look, and personalization lives in the *words*.

Fill the style's `{{tokens}}` from `campaign.md`'s **Delivery style** block (+ `BRAND.md`): the channel
link, WhatsApp, WeChat, the searchable subject prefixes (EN/ZH), the sign-off, the highlight color.
**Ask only for what's missing.** Write the resolved values to `outbox/_style.json` (the preview/build
step reads it). Never hardcode contact values in the skill — they come from the campaign.

## Step 2 — Assemble the ✅ emails
1. **Select only `✅` leads.** Skip `🟡`/`❌`/`⚠️` unless the user explicitly includes them.
2. For each ✅ section, parse `{ name, email, subject, body }` from its **SEND** block + the lead's
   email (from the CSV). Decide **language** per the language rule (Chinese if the channel name/handle
   has Chinese characters or the research says a Chinese audience; else English) — the drafts from
   `leads-research` already follow the right structure and language.
3. Confirm each body has the structure (greeting · 2 bullets · one **bold** reason · exactly one
   `==highlight==` invite · welcoming close · correct signature — WeChat only on Chinese), the
   searchable subject prefix, **one** YouTube link, and **no view counts / no "viral."** Fix any that
   drifted before previewing.
4. Write the selected emails to `outbox/_emails.json` — `[{name, email, subject, body, lang}]`.

## Step 3 — Build the three previews (before the gate)
Run `scripts/build_previews.py` (see `references/preview-pages.md`) to write, into
`lead-system/<campaign>/outbox/`:
- `_send-preview.md` — every exact email as text.
- `_preview.html` — every email rendered exactly as it sends (open in a browser to eyeball it).
- `_preview-redacted.html` — same, but recipient email + WhatsApp + WeChat blacked out (shareable);
  the YouTube link stays.
- `_send.json` — the exact HTML body each send passes verbatim (so the preview == what sends).

```bash
python3 scripts/build_previews.py \
  --emails lead-system/<campaign>/outbox/_emails.json \
  --config lead-system/<campaign>/outbox/_style.json \
  --out    lead-system/<campaign>/outbox/
```

## The send gate (mandatory — never skip)
Real email is irreversible and outward-facing. Before any send:
1. **Show the user:** the **count** to be sent, the recipient list (names), and the **first 2 full
   emails verbatim** (from `_send-preview.md` / `_preview.html`).
2. **Get an explicit go** ("send these N?"). Only on a clear yes do you send. If the user says
   "drafts" or "outbox", switch to that mode instead.

This gate is required even if the user said "just send" earlier — confirm the *final* count + sample
once, at send time. (It's one confirmation, not a per-email nag.)

## Step 4 — Choose the send transport (ask once)
**How the email actually leaves depends on the host — so ask, don't assume.** Read
`references/gmail-setup.md` and pick with the user (use `AskUserQuestion`). The first that fits, in
rough order of "actually sends without a human click":

- **A · Automation send node (real send).** A workflow tool that takes **To / Subject / Message** and
  sends. The validated reference path is the **n8n "Send a message in Gmail"** node (Message = the HTML
  body). **make.com / Zapier / a custom MCP or webhook** expose the same `To / Subject / Message(HTML)`
  shape — use whichever the user has wired. **One tool call per recipient = one real email sent** (not
  a draft).
- **B · Gmail MCP** — a connected Gmail MCP server's `send_email` / `create_draft` tool.
- **C · Gmail API / CLI** — terminal hosts (OAuth; `users.messages.send` or `drafts.create`).
- **D · Outbox folder** — no integration / dry run: write copy-paste drafts (see Mode D below).

> Because the send node sends **HTML**, the Message must be the rendered HTML (`<p>/<br>/<ul>/<strong>/
> <mark>`) — plain-text newlines get collapsed. That HTML is exactly `_send.json[i].html` from Step 3,
> so what the user approved in `_preview.html` is byte-for-byte what sends.

## The sending loop (one recipient at a time)
```
for each ✅ lead (skip any already in sent.log):
    msg = _send.json entry for this lead         # To, Subject, Message(HTML) — matches the preview
    call the chosen transport ONCE  →  To: <this one address>   (n8n node / MCP / API)
    append to sent.log (timestamp, recipient, subject)  →  pace before the next
```
- **One call per recipient.** Never BCC/bulk — every email is different, and 1:1 sends keep
  deliverability high.
- **Never send to a lead with no email.** Skip and report it.
- **Pace it.** Short gap between sends; **cap ~25 per sending mailbox per day**. On hundreds of leads,
  send up to the daily cap, log the rest as `pending`, resume next run — never fire them all at once.
- **Resume-safe.** Check `sent.log` first; skip anyone already sent so a re-run never double-sends.
- **Report** sent / failed / skipped in one summary line. Stop on repeated failures (bad auth, rate
  limit) — report, don't blindly retry.

## Sending modes (detail)

### Mode A — Automation send node (primary when connected)
The n8n "Send a message in Gmail" node (or a make.com/Zapier/custom-MCP equivalent) takes
**To / Subject / Message**. Set the node to **HTML**, pass `_send.json[i].html` as Message, loop one
call per recipient. This is a **real send** — the send gate above is the only approval. Setup details
+ the make.com/Zapier/MCP variants: `references/gmail-setup.md`.

### Mode B/C — Gmail MCP or Gmail API
Use a connected Gmail MCP's `send_email`/`create_draft`, or the Gmail API on a terminal host. Prefer
**creating Gmail drafts** when the user wants a last human look in their own inbox; **send** only on an
explicit go. From-address = the user's Gmail.

### Mode D — Outbox folder (no integration / dry run)
If nothing is connected (or the user wants a dry run), write one file per ✅ lead to
`lead-system/<campaign>/outbox/` alongside the previews:
```
outbox/
├── 001-<lead-slug>.md      # To / Subject / Body — copy-paste ready
└── _index.md               # table: lead · email · subject · status
```
Tell the user exactly how to send (paste into Gmail, or connect a transport and re-run in send mode).

## Safety rules
- **Only ✅ leads** unless told otherwise. **Build the preview, confirm count + sample, never auto-blast.**
- **One send per lead** — check `sent.log` so a re-run doesn't double-send.
- Respect unsubscribes / do-not-contact if the CSV marks any. Don't send to leads missing an email.
- If sending many, pace batches and stop on repeated failures (bad auth, rate limit) — report, don't
  blindly retry.

## Output contract
- Writes the three previews (`_send-preview.md`, `_preview.html`, `_preview-redacted.html`) + `_send.json`.
- Sends ✅ emails via the chosen transport **after** the count+sample confirmation, OR writes `outbox/`
  drafts.
- Writes `sent.log`. Reports sent / failed / skipped counts in one summary line.
