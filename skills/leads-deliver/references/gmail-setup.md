# Gmail setup (for the agent + the user)

`leads-deliver` needs a way to create drafts or send mail from the user's Gmail. The right path
depends on the host. Detect what's available, in this order, and guide the user to the first that fits.

## Option 1 — Gmail MCP server (best for Claude Code & Claude Cowork)

If a Gmail MCP server is connected, use its draft/send tool directly (discover it via the host's
tool list / ToolSearch). Common ones expose `create_draft`, `send_email`, `list_messages`.

Set up (user runs this in their terminal):
```bash
# Example shape — exact command depends on the MCP server chosen:
claude mcp add gmail -- npx -y <gmail-mcp-package>
```
Then authenticate via the server's OAuth flow (it opens a Google consent screen once; tokens are
stored locally). After connecting, **restart the host** so the tool is available.

Eric Tech's `ops-brain` plugin also provides Gmail sync / email responses — if it's installed, its
Gmail capability can back this step.

## Option 2 — Gmail API via CLI / OAuth (terminal hosts)

For a CLI host without MCP, use the Gmail API:
1. Create a Google Cloud project, enable the **Gmail API**, create an **OAuth client (Desktop)**.
2. Download the client secret; run a one-time OAuth flow to get a refresh token (store it in a
   gitignored local file or env var — never commit it).
3. Use the Gmail API `users.messages.send` (or `drafts.create`) endpoint, base64url-encoding an
   RFC 822 message.

This is more setup; prefer Option 1 if the host supports MCP.

## Option 3 — Outbox folder (no Gmail / dry run)

No Gmail configured? `leads-deliver` writes copy-paste-ready drafts to
`lead-system/<campaign>/outbox/` and tells the user to paste them, or to connect Gmail (Option 1)
and re-run in send mode. This always works, with zero credentials.

## Security
- **Never commit credentials.** Refresh tokens / client secrets go in a gitignored local file or env
  var (the repo `.gitignore` already excludes `.env*` and `*.local.json`).
- Send **from the user's own Gmail**, with their explicit go at the send gate.
- Prefer **creating drafts** for a final human look unless the user has approved sending.
