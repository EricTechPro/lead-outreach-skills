# Install

Two ways in. Either hand the repo to your agent (recommended) or run the installer yourself.

## A. Let your agent install it (recommended)

Paste this to Claude Code / Cowork:

```
Install the Lead Outreach skills into this project.
Repo: https://github.com/EricTechPro/lead-outreach-skills
Read the repo's docs/install.md and follow it.
```

Works on **both Claude Code and Claude Cowork** — the agent picks the right path:
- **Claude Code** (has a shell): it clones the repo and runs `install.sh`.
- **Claude Cowork** (sandboxed — no git/npm): it adds the repo as a plugin, or copies the skill +
  command + template files into the workspace with its file tools. No shell needed.

(Agent-facing detail for both paths lives in [docs/install.md](docs/install.md).)

## B. Install it yourself

### Claude Code (shell)
```bash
git clone https://github.com/EricTechPro/lead-outreach-skills /tmp/lead-outreach-skills
bash /tmp/lead-outreach-skills/install.sh "$PWD"      # this project
# or
bash /tmp/lead-outreach-skills/install.sh --global    # all projects (~/.claude)
```

### Claude Cowork (no shell)
Add the repo as a **plugin** (from `.claude-plugin/marketplace.json`), or ask the agent: *"copy the
three lead-outreach skills + commands from EricTechPro/lead-outreach-skills into this workspace's
`.claude/`."* Cowork can't run `install.sh`/`npx` — that's expected.

Either way you get three skills (`.claude/skills/`), three slash commands (`.claude/commands/`), and
the example templates (`_templates/`). The skills are self-contained — they work in an empty project.

## Connect the research engine

The skills drive tools the host already provides; there's no NotebookLM dependency and no daily cap.

1. **Firecrawl** (websites + footprint). The skill auto-detects the access method (MCP → CLI → curl) —
   set up whichever fits your host:
   - **Claude Code (recommended):** one command installs the official Firecrawl CLI + skill + auth:
     ```bash
     npx -y firecrawl-cli@latest init --all --browser
     ```
   - **Claude Cowork:** connect the **Firecrawl MCP** (official Claude plugin) — the sandbox usually
     can't run the CLI.
   - **Fallback (any shell):** free key at https://www.firecrawl.dev, then:
     ```bash
     echo 'export FIRECRAWL_API_KEY="fc-YOUR-KEY"' >> ~/.zshrc && source ~/.zshrc
     ```
   CLI/MCP read the key on launch — **restart the host** after setting it. (Keep the key out of git —
   it lives in your shell rc, not a committed file.)

2. **YouTube** (channels) — make sure the host has YouTube tooling (vidiq MCP, or a YouTube Data /
   transcript tool). Without it, the YouTube branch falls back to web search.

3. **Gmail** — only for `/leads-deliver` *send* mode. See
   [`skills/leads-deliver/references/gmail-setup.md`](skills/leads-deliver/references/gmail-setup.md):
   MCP (best), CLI/API, or the zero-setup `outbox/` folder. `/leads-deliver` works with no Gmail at
   all — it just writes drafts you can paste.

## Verify

In your host:
```
/leads-plan
```
If it responds asking for your context/offer, you're installed. Then:
```
/leads-research ./_templates/leads.example.csv
```
runs the engine over the sample leads.
