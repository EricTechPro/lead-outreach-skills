# Prerequisites — exact setup for each dependency

The three skills drive tools your host provides. You don't need all of them to start — only
**Firecrawl** (or any web tool) is needed to research; YouTube and Gmail are optional upgrades. Set
up what you need, in this order. `/leads-research` will **preflight-test** these and point you back
here if something isn't working.

---

## 1. Firecrawl — website + footprint research (required)

The skill auto-detects the access method. Set up **one** that fits your host:

### Claude Code (recommended) — official CLI + skill, one command
```bash
npx -y firecrawl-cli@latest init --all --browser
```
Installs the `firecrawl` CLI, opens a browser to authenticate, and adds Firecrawl's own skill.
Verify:
```bash
firecrawl scrape https://example.com --json
```

### Claude Cowork — Firecrawl MCP (the sandbox can't run the CLI)
Firecrawl is an official Claude plugin. Connect the **Firecrawl MCP** in your host's plugin/MCP
settings (or `claude mcp add firecrawl -- npx -y firecrawl-mcp` on a host that supports it), then
authenticate. The skill calls `firecrawl_scrape` / `firecrawl_search`.

### Any shell host — API key (fallback)
1. Get a **free key** at https://www.firecrawl.dev → Dashboard → API Keys (looks like `fc-…`).
2. Put it in your shell env (gitignored — never a committed file):
   ```bash
   echo 'export FIRECRAWL_API_KEY="fc-YOUR-KEY"' >> ~/.zshrc && source ~/.zshrc
   ```
3. **Restart the host** so the MCP/CLI picks it up.

**Test it:**
- **Claude Code:** `bash .claude/skills/leads-research/scripts/preflight.sh` → expect `✓ … Engine ready`.
- **Claude Cowork:** no shell — the `leads-research` preflight tests the **MCP** directly with a tiny
  `firecrawl_scrape` call on `example.com`. You don't run anything by hand.

---

## 2. YouTube tooling — channel research (optional, recommended)

Without this, the YouTube branch falls back to plain web search (shallower — no sub counts, growth,
or top-video signals).

### vidiq MCP (what Eric Tech uses)
Requires a vidiq account. Connect the **vidiq MCP** server in your host's MCP settings (per vidiq's
own setup). The skill uses `vidiq_channel_stats` and `vidiq_channel_videos`.

### Alternatives
- Any **YouTube Data API** MCP/tool (channel stats + video lists) works — the skill adapts.
- A **transcript** tool (e.g. a YouTube transcript MCP) adds depth for the top 1–3 videos.
- **None?** The skill uses web search for "<channel> subscribers" + top video titles. It says so in
  the preflight readiness line.

**Test it:** the skill pings `vidiq_channel_stats` on a known handle (e.g. `@mkbhd`) during preflight.

---

## 3. Gmail — only for `/leads-deliver` *send* mode (optional)

Not needed to plan, research, or write drafts. `/leads-deliver` works with **zero** Gmail setup by
writing copy-paste-ready files to `outbox/`. Set up Gmail only when you want it to create/send mail
directly. Full detail in [`skills/leads-deliver/references/gmail-setup.md`](../skills/leads-deliver/references/gmail-setup.md).

### Claude Code — Gmail MCP (recommended)
Add a Gmail MCP server from the terminal:
```bash
claude mcp add gmail -- npx -y <gmail-mcp-package>   # e.g. GongRzhe/Gmail-MCP-Server
```
Authenticate via its one-time Google OAuth (consent screen; tokens stored locally). **Restart the
host.** Eric Tech's `ops-brain` plugin also provides Gmail capability if installed.

### Claude Cowork — connector vs. send (important nuance)
- **Native Google Workspace connector** = **drafts + read only**. Claude creates the draft in your
  Gmail with your approval; **you click send manually**. Safest, but not auto-send.
- **To actually send from Cowork**, add a **third-party Gmail MCP** (e.g. Composio Gmail, CAMC, or
  GongRzhe's server) via the host's **Connectors / Plugins** menu, then authenticate in the UI. Those
  expose a send/draft tool the agent can call. (Note: Cowork's Gmail MCP currently can't attach files
  to drafts — body/subject/cc/bcc only. We don't attach anyway.)
- No terminal in Cowork — always use the Connectors/Plugins UI, not `claude mcp add`.

### Gmail API via CLI (Claude Code without MCP)
Enable the Gmail API in a Google Cloud project, create an OAuth **Desktop** client, run the one-time
flow for a refresh token (store it in a gitignored local file / env var — never commit it).

**Test it:** `/leads-deliver` preflights Gmail (lists labels or creates a throwaway draft) and shows a
rendered sample before any send.

---

## At a glance

| Tool | Required? | Fastest setup | Skill tests it? |
|---|---|---|---|
| **Firecrawl** | Yes (or any web tool) | `npx -y firecrawl-cli@latest init --all --browser` | ✅ preflight scrape |
| **YouTube / vidiq** | Optional (falls back to search) | connect vidiq MCP | ✅ preflight ping |
| **Gmail** | Optional (else `outbox/` drafts) | connect a Gmail MCP | ✅ before send |

Secrets (API keys, OAuth tokens) live in your shell env or gitignored local files — the repo
`.gitignore` already excludes `.env*` and `*.local.json`.
