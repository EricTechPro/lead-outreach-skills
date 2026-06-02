---
description: Research every lead in a CSV into a reviewable leads-spec.md — per-lead dossier (who / fit verdict / drafted email), source-attributed, no email sent
---

Invoke the **leads-research** skill to research the leads.

What the user gave you (a path to a leads CSV, and optionally a campaign.md):

$ARGUMENTS

Follow the skill: read `campaign.md` for the goal, research each lead via the engine router
(YouTube → vidiq/transcript, website → Firecrawl, gaps → web search), and write one scannable
section per lead into `leads-spec.md` (✅/🟡/❌ fit verdict, source-attributed claims, drafted
email). Do NOT send anything — that is the `/leads-deliver` step.
