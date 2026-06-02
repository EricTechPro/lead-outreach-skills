# Research router

Route by the source type the lead actually has. One tool per job — never one tool for everything.
The goal is a *lean* dossier: enough to judge fit and personalize a message, not a biography.

## Accessing Firecrawl (host-agnostic — detect, don't assume)

Firecrawl is reachable three ways. **Detect what the host has and use the first available**, in this
order — don't hard-code one. The website + footprint steps below work the same regardless of method.

1. **Firecrawl MCP tool** — if the host exposes `firecrawl_scrape` / `firecrawl_search` (discover via
   the tool list / ToolSearch). **Best on Claude Cowork** (sandboxed — no shell), and fine anywhere
   MCP is connected. Call the tool with the same `url` + JSON-extraction `prompt` shown below.
2. **Firecrawl CLI** — if the `firecrawl` command is on PATH (`firecrawl/cli`). **Best on Claude Code**
   (terminal). Reads `FIRECRAWL_API_KEY` from env automatically:
   ```bash
   firecrawl scrape "https://<lead-site>/" --json --prompt "Extract: name, role, offer, pricing, value prop, all links"
   firecrawl search "<lead name> <niche> podcast collaboration" --limit 6 --json
   ```
3. **Raw API (curl)** — universal fallback for any shell host with `FIRECRAWL_API_KEY` set (the curl
   forms shown in the sections below).

Cowork can't usually run the CLI (sandboxed); Claude Code can use any of the three. If none is
available (no MCP, no CLI, no key), say so and fall back to the host's generic web-search tool for
the website/footprint steps — don't silently skip a lead.

## YouTube channel → YouTube-native tools (NOT Firecrawl)

YouTube channel pages are JavaScript walls — scrapers get almost nothing. Use the host's YouTube
tools instead. With vidiq MCP available (Eric Tech's stack):

- **`vidiq_channel_stats`** (handle or channel ID, e.g. `@nateherk`) → subs, total views, video
  count, **30-day growth**, topics, country. Growth + size = the first fit signal.
- **`vidiq_channel_videos`** (`popular: true`) → their **top videos**. The *titles alone* reveal
  positioning, audience, and what works for them. This is the single highest-signal call.
- **`vidiq_channel_videos`** (`popular: false`) → recent uploads → what they're focused on *now*.
- **Transcript of the top 1–3 videos** (host transcript tool) → only when you need depth on *how*
  they do something (e.g. how they run a collab/podcast). Don't transcribe more than you need.

No vidiq? Fall back to the host's YouTube Data / transcript tools, or a web search for
`"<channel>" subscribers` + their top video titles.

**What you extract:** size + growth, their core topic/positioning, what formats work, any collab/
guest pattern, and the single most relevant overlap with the campaign goal.

## Website → Firecrawl scrape with JSON extraction

Firecrawl is the right tool for the *website* half of a lead. Use JSON format with a prompt — never
dump the whole page when you want specific fields. Call it via whichever access method the host has
(MCP tool / CLI / curl — see "Accessing Firecrawl" above). The API/curl form:
```bash
curl -s -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://<lead-site>/",
       "formats":[{"type":"json","prompt":"Extract: name, role/title, what they offer or sell, pricing if shown, the one-line value proposition, and all external/social links."}]}'
```
**What you extract:** who they are, their offer/product, pricing/positioning, and the full link set
(LinkedIn, other socials, press) — which seeds further footprint research.

> Connecting Firecrawl: easiest is the official setup — `npx -y firecrawl-cli@latest init --all --browser`
> (installs the CLI + the official Firecrawl skill + browser auth). Or set `FIRECRAWL_API_KEY` in your
> shell env (free key from firecrawl.dev) for curl, or connect the Firecrawl MCP (best on Cowork).
> MCP/CLI read the key on launch — restart the host after setting it. See `docs/install.md`.

## Footprint / recent context → web search or Firecrawl search

Find press, podcast appearances, communities, recent moves, and named collaborators. Use the
Firecrawl MCP `firecrawl_search` tool, `firecrawl search … --json` (CLI), or the API/curl form:
```bash
curl -s -X POST https://api.firecrawl.dev/v2/search \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"<lead name> <niche> podcast interview collaboration","limit":6}'
```
Search-result titles + snippets + URL tags often carry the answer (e.g. a podcast episode whose link
is tagged with the guest's name). **Always keep the source URL** for anything you carry into the
dossier — search blends entities, so confirm a fact belongs to *this* lead before using it.

## Cost discipline
- Start with the cheapest high-signal call (channel stats + top video titles, or one website scrape).
- Add a transcript / extra searches only when the dossier still can't judge fit or personalize.
- Record every source URL as you go — the spec format requires them.
