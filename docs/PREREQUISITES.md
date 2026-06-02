# Prerequisites — exact setup per host

The three skills drive tools your host provides. **Only Firecrawl (or any web tool) is required** to
research; YouTube and Gmail are optional. `/leads-research` preflight-tests these and points you back
here if something isn't connected.

Pick your host:
- **[Claude Code](#claude-code-terminal)** — set tools up with terminal commands.
- **[Claude Cowork](#claude-cowork-connectors-ui)** — set tools up by clicking in the Connectors UI.

| Tool | Required? | Claude Code | Claude Cowork |
|---|---|---|---|
| **Firecrawl** | yes (or any web tool) | CLI / API key | **custom connector** (`mcp.firecrawl.dev`) |
| **YouTube / vidiq** | optional (falls back to web search) | vidiq MCP | connector if available, else skip |
| **Gmail** | optional (else `outbox/` drafts) | Gmail MCP / API | built-in **Gmail** connector |

---

# Claude Code (terminal)

## 1. Firecrawl — website + footprint (required)
Pick one:
- **Official CLI + skill (recommended):**
  ```bash
  npx -y firecrawl-cli@latest init --all --browser
  ```
  Verify: `firecrawl scrape https://example.com --json`
- **MCP server:**
  ```bash
  claude mcp add firecrawl -- npx -y firecrawl-mcp     # set FIRECRAWL_API_KEY first
  ```
- **API key only (curl fallback):** free key at https://www.firecrawl.dev, then
  ```bash
  echo 'export FIRECRAWL_API_KEY="fc-YOUR-KEY"' >> ~/.zshrc && source ~/.zshrc
  ```
**Restart the host** after setting the key. **Test:** `bash .claude/skills/leads-research/scripts/preflight.sh`.

## 2. YouTube / vidiq — channel research (optional)
vidiq has a **hosted MCP** — add it as a remote MCP server:
```bash
claude mcp add --transport http vidiq https://mcp.vidiq.com/mcp     # then authenticate (API key or OAuth)
```
- Get an **API key** from your vidiq account, or complete the OAuth sign-in on connect.
- **Read-only** (stats, top videos, competitors, keywords) — it can't change your channel.
- Requires a vidiq **Max** plan. Any other YouTube Data / transcript MCP works too.
- No YouTube tool? The skill **falls back to web search** (shallower). **Test:** preflight pings `@mkbhd`.

## 3. Gmail — only for `/leads-deliver` send mode (optional)
```bash
claude mcp add gmail -- npx -y <gmail-mcp-package>    # e.g. GongRzhe/Gmail-MCP-Server
```
Authenticate via its one-time Google OAuth. Or use the Gmail API with an OAuth Desktop client + a
refresh token (store it in a gitignored file — never commit). No Gmail at all → `/leads-deliver`
writes `outbox/` drafts.

---

# Claude Cowork (connectors UI)

Cowork has **no terminal** — you add everything as **connectors** by clicking. There are two kinds:
built-in connectors (search and toggle on) and **custom connectors** (paste a remote MCP URL).

**How to open the connectors menu (do this first):**
1. In the chat composer, click the **`+`** button (bottom-left).
2. Click **Connectors**.
3. Click **Add connector** (or **Manage connectors** to see what's already there).
4. From here you can **search/browse** built-in connectors, or choose **Add custom connector** to
   paste a URL.

## 1. Firecrawl — website + footprint (required) → custom connector
Firecrawl isn't in the built-in connector list, so add it as a **custom connector**:
1. **`+` → Connectors → Add connector → Add custom connector**.
2. **Server URL:** paste
   ```
   https://mcp.firecrawl.dev/v2/mcp
   ```
3. **Auth:** choose **Bearer Token** and paste your Firecrawl API key (`fc-…`, free from
   [firecrawl.dev](https://www.firecrawl.dev) → Dashboard → API Keys).
4. Click **Add**, then back in **`+` → Connectors** toggle **Firecrawl ON** for the chat.
5. **Test:** the `leads-research` preflight calls `firecrawl_scrape` on `example.com` automatically —
   no command to run by hand.

## 2. Gmail — only for sending (optional) → built-in connector
1. **`+` → Connectors → Add connector**.
2. **Search "Gmail"** in the connector list → add it → complete the **Google sign-in** popup.
3. Toggle **Gmail ON** for the chat.
4. ⚠️ The **native Gmail connector is drafts-only** — Claude creates the draft, *you* click send. To
   send automatically, add a **third-party Gmail connector** instead (Composio / CAMC) via *Add
   custom connector* with that provider's MCP URL. Otherwise `/leads-deliver` runs in draft mode.

## 3. YouTube / vidiq — channel research (optional) → custom connector
vidiq has a hosted MCP, so add it as a **custom connector** (same flow as Firecrawl):
1. **`+` → Connectors → Add connector → Add custom connector**.
2. **Server URL:** paste
   ```
   https://mcp.vidiq.com/mcp
   ```
3. **Auth:** **API key** (from your vidiq account — simplest) or **OAuth** (sign in on connect).
4. Click **Add**, then toggle **vidiq ON** for the chat.
5. Notes: **read-only** (stats / top videos / competitors / keywords); requires a vidiq **Max** plan.
6. Can't / don't want to? **Skip it** — YouTube research falls back to web search (shallower). The
   preflight readiness line tells you which path is active.

> **Recommended Cowork order:** connect these connectors **first**, then add the skill
> (**`+` → Add plugins…** or **Skills**). Then `/leads-research` preflights green with no prompts.
> Note: custom connectors run from Anthropic's cloud, so the MCP URL must be reachable on the public
> internet — Firecrawl's hosted URL already is.

---

## Secrets
API keys / OAuth tokens live in your shell env, a gitignored local file, or the connector's own
secure storage — **never a committed file**. The repo `.gitignore` already excludes `.env*` and
`*.local.json`.
