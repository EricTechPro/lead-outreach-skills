# Install instructions (for the agent)

You are installing the **lead-outreach** skills into the user's current project. Do this:

1. **Clone the repo** into a temporary location (or use it if already cloned):
   ```bash
   git clone https://github.com/EricTechPro/lead-outreach-skills /tmp/lead-outreach-skills
   ```

2. **Run the installer** targeting the user's current project (default) or globally:
   ```bash
   bash /tmp/lead-outreach-skills/install.sh "$PWD"      # this project
   # or: bash /tmp/lead-outreach-skills/install.sh --global   # all projects (~/.claude)
   ```
   This copies the three skills into `.claude/skills/`, the three slash commands into
   `.claude/commands/`, and example templates into `_templates/`. The skills are self-contained
   (copywriting rules are bundled), so they work in an empty project with nothing else installed.

3. **Connect the research engine** (the skills use the host's tools — no NotebookLM needed):
   - **Firecrawl** (website + footprint research): get a free key at https://www.firecrawl.dev, then
     ```bash
     echo 'export FIRECRAWL_API_KEY="fc-YOUR-KEY"' >> ~/.zshrc && source ~/.zshrc
     ```
     If the host uses a Firecrawl MCP server, it reads this env var on launch — **restart the host**
     after setting it.
   - **YouTube** (channel research): ensure the host has YouTube tooling (e.g. the vidiq MCP, or a
     YouTube Data / transcript tool). The skill falls back to web search if none is present.

4. **(Optional) Gmail** — only needed for `/leads-deliver` *send* mode. See
   `skills/leads-deliver/references/gmail-setup.md` (MCP, CLI/API, or the zero-setup outbox folder).
   `/leads-deliver` works with no Gmail at all by writing copy-paste drafts to `outbox/`.

5. **Install Python deps** (currently a no-op — present for future helper scripts):
   ```bash
   pip install -r /tmp/lead-outreach-skills/requirements.txt
   ```

6. **Confirm** the three skills + commands are discoverable, then tell the user:
   > "Installed. Start with `/leads-plan ./_context` to define your offer, then
   > `/leads-research <your-leads.csv>`."

Do not require Superpowers, NotebookLM, or any other repo. If `install.sh` reports a missing skill or
command, stop and show the user the exact line.
