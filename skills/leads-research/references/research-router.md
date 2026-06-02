# Research router

Route by the source type the lead actually has. One tool per job — never one tool for everything.
The goal is a *lean* dossier: enough to judge fit and personalize a message, not a biography.

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
dump the whole page when you want specific fields.

Via the Firecrawl MCP tool (`firecrawl_scrape`), or the API directly:
```bash
curl -s -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://<lead-site>/",
       "formats":[{"type":"json","prompt":"Extract: name, role/title, what they offer or sell, pricing if shown, the one-line value proposition, and all external/social links."}]}'
```
**What you extract:** who they are, their offer/product, pricing/positioning, and the full link set
(LinkedIn, other socials, press) — which seeds further footprint research.

> Connecting Firecrawl: set `FIRECRAWL_API_KEY` in your shell env (a free key from firecrawl.dev).
> The MCP server reads it on launch — restart the host after setting it. See `docs/install.md`.

## Footprint / recent context → web search or Firecrawl search

Find press, podcast appearances, communities, recent moves, and named collaborators.
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
