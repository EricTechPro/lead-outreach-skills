# Install instructions (for the agent)

You are installing the **lead-outreach** skills into the user's current project/workspace. There are
two paths — pick the one for your host. The end state is identical: three skills in
`.claude/skills/`, three commands in `.claude/commands/`, examples in `_templates/`.

---

## Path A — Claude Code (has a shell)

1. **Clone** into a temp location:
   ```bash
   git clone https://github.com/EricTechPro/lead-outreach-skills /tmp/lead-outreach-skills
   ```
2. **Run the installer** (project default, or `--global`):
   ```bash
   bash /tmp/lead-outreach-skills/install.sh "$PWD"
   ```
3. **Python deps** (currently a no-op, safe to run): `pip install -r /tmp/lead-outreach-skills/requirements.txt`

If `install.sh` reports a missing skill/command, stop and show the user the exact line.

---

## Path B — Claude Cowork (sandboxed — no git/npm/shell)

Cowork can't clone, run `install.sh`, or run `npx`. Recommended order: **connect your connectors
first, then add the skill** — so the skill's preflight finds a live engine immediately.

**Step 1 — connect the connectors** (the `+` menu in the composer):
- **`+` → Connectors → Add connector** → add **Firecrawl** and paste your API key (required for
  research). For sending, also add **Gmail** (it's in the connector list — note the native Gmail
  connector is *drafts only*; for true auto-send add a third-party Gmail connector here). Add
  **vidiq** via *Add connector* too if you have it (optional — else YouTube falls back to web search).
- Toggle each connector **on**. Authenticate in the popups.

**Step 2 — add the skill** (no shell needed):
- **`+` → Add plugins…** → add this repo as a plugin via its `.claude-plugin/marketplace.json`
  (`EricTechPro/lead-outreach-skills`), **or**
- **`+` → Skills**, or copy the files with your read/write tools:
  - `skills/leads-plan/`, `skills/leads-research/`, `skills/leads-deliver/` (whole folders, incl.
    `references/` and `scripts/`) → `.claude/skills/<name>/`
  - `commands/*.md` → `.claude/commands/` · `_templates/*` → `_templates/` at the workspace root
  Preserve the structure exactly. No chmod needed (the preflight `.sh` isn't used on Cowork — the
  skill tests the MCP connectors directly).

**Step 3** — confirm the three skills + commands are discoverable; the connectors from Step 1 are
already live, so `/leads-research` preflights green with no extra setup.

---

## 3. Connect the research engine (both paths — no NotebookLM needed)

The skill **auto-detects** the access method. Set up whichever fits the host (full step-by-step in
**[PREREQUISITES.md](PREREQUISITES.md)**):

- **Firecrawl** (website + footprint):
  - **Claude Code:** `npx -y firecrawl-cli@latest init --all --browser` (CLI + skill + auth), or set
    `FIRECRAWL_API_KEY` in the shell for curl.
  - **Claude Cowork:** connect the **Firecrawl MCP** (official Claude plugin) — the skill calls
    `firecrawl_scrape` / `firecrawl_search`. The CLI/curl/preflight-script paths don't apply in the
    sandbox; the skill tests the MCP with a tiny `firecrawl_scrape` call instead.
- **YouTube** (channel research): connect the vidiq MCP (or any YouTube Data / transcript tool). Both
  hosts use MCP tools here. Falls back to web search if absent.

## 4. (Optional) Gmail — only for `/leads-deliver` send mode
See `skills/leads-deliver/references/gmail-setup.md`. **Both Claude Code and Cowork should use the
Gmail MCP** (Cowork has no shell for the CLI/API path). With no Gmail at all, `/leads-deliver` writes
copy-paste drafts to `outbox/` — works everywhere.

## 5. Confirm
Tell the user:
> "Installed. Start with `/leads-plan ./_context` to define your offer, then
> `/leads-research <your-leads.csv>`. I'll preflight-test Firecrawl before researching."

Do not require Superpowers, NotebookLM, the Firecrawl CLI, or any other repo. The skills are
self-contained and run on MCP tools alone (Cowork) or shell tools (Claude Code).
