# Send setup (for the agent + the user)

`leads-deliver` needs a way to send (or draft) mail from the user's Gmail. **The right path depends on
the host — so the skill asks which transport the user has, it does not assume one.** Detect what's
available, guide the user to the first that fits, and use it for one 1:1 send per recipient.

The send body is **HTML** (so bullets/bold/the one highlight render). Any transport that takes a
message must be set to **HTML** and given `_send.json[i].html` — plain-text newlines get collapsed.

## Option 1 — Automation send node (n8n / make.com / Zapier / custom MCP)  ← primary when connected

A workflow tool exposes one action that takes **To / Subject / Message** and sends through the user's
Gmail. **One call per recipient = one real email sent** (not a draft). The send gate is the approval.

**n8n — the validated reference path.** The **"Send a message in Gmail"** node:
- Inputs: **To**, **Subject**, **Message**. Set the node/parameter to **HTML** and pass the rendered
  HTML body as **Message**.
- Trigger it once per recipient (e.g. via its tool/webhook the host can call), looping the ✅ leads.
- It sends immediately — there is no draft step, so rely on the count+sample gate before the loop.

**make.com / Zapier / a custom MCP or webhook** expose the **same `To / Subject / Message(HTML)`
shape** — a "Gmail → Send Email" module, a webhook that forwards to Gmail, or an MCP `send` tool. Use
whichever the user already has wired; the loop is identical. If the user is on Claude Cowork, this is
usually how they get a true auto-send (the native Workspace connector only drafts — see the caveat
below).

> Keep one call per recipient (no bulk/BCC), set HTML, and send the exact `_send.json` body so what was
> previewed is what sends.

## Option 2 — Gmail MCP server (Claude Code & Cowork)

If a Gmail MCP server is connected, use its draft/send tool directly (discover it via the host's tool
list / ToolSearch). Common ones expose `create_draft`, `send_email`, `list_messages`.

Set up (user runs this in their terminal):
```bash
# Example shape — exact command depends on the MCP server chosen:
claude mcp add gmail -- npx -y <gmail-mcp-package>
```
Authenticate via the server's OAuth flow (a Google consent screen once; tokens stored locally), then
**restart the host** so the tool is available. Eric Tech's `ops-brain` plugin, if installed, can also
back this step.

**Cowork caveat (sending vs drafts):** the **native Google Workspace connector creates drafts only — it
will not auto-send** (the user clicks send). To send programmatically from Cowork, use an **automation
send node (Option 1)** or a **third-party Gmail MCP** (Composio Gmail / CAMC / GongRzhe) via the
Connectors/Plugins UI. If only the native connector is present, run in **draft mode** and tell the user
to send from Gmail.

## Option 3 — Gmail API via CLI / OAuth (terminal hosts)

For a CLI host without MCP, use the Gmail API:
1. Create a Google Cloud project, enable the **Gmail API**, create an **OAuth client (Desktop)**.
2. Download the client secret; run a one-time OAuth flow for a refresh token (store it in a gitignored
   local file or env var — never commit it).
3. Call `users.messages.send` (or `drafts.create`), base64url-encoding an RFC 822 message (set the HTML
   part as `text/html`).

More setup; prefer Option 1 or 2 if the host supports them.

## Option 4 — Outbox folder (no integration / dry run)

No transport configured? `leads-deliver` writes copy-paste-ready drafts to
`lead-system/<campaign>/outbox/` (alongside the previews) and tells the user to paste them, or to
connect a transport and re-run in send mode. Always works, zero credentials.

## Security
- **Never commit credentials.** Refresh tokens / client secrets / webhook URLs go in a gitignored local
  file or env var (the repo `.gitignore` already excludes `.env*` and `*.local.json`).
- Send **from the user's own Gmail**, with their explicit go at the send gate.
- Prefer **creating drafts** for a final human look unless the user has approved sending.
- An automation send node (Option 1) sends for real with no draft step — only run it after the gate.
