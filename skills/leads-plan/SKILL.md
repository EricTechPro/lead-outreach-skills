---
name: leads-plan
description: Plan an outreach campaign — clarify who you are, what you sell, and who you're targeting, using the value-equation framing, and write a short reviewable campaign.md. Use whenever the user wants to start lead outreach, define an outreach goal/offer/ICP, or prep a list of leads for personalized email — before any lead is researched. Reads an existing context/brand folder if one is given (asks for the path if it can't find one). Also /leads-plan. NOT for researching individual leads (use leads-research) and NOT for sending email (use leads-deliver).
---

# Leads — Plan

The brain of the pipeline. Before researching a single lead, get crisp on **who you are, what you
offer, and who you're targeting** — because that goal is the north star every per-lead message is
written against. Output is one short, scannable `campaign.md` the user approves.

This skill writes the goal only. `leads-research` uses it to research leads; `leads-deliver` sends.

## When to use
- "Plan an outreach campaign to these leads"
- "I want to reach out to a list — help me define the offer first"
- `/leads-plan`

## When NOT to use
- The user already has an approved `campaign.md` and a CSV → `leads-research`
- The user wants to send already-approved messages → `leads-deliver`

## The campaign folder it creates
Everything for one campaign lives under the **current project root**, one folder per campaign:
```
lead-system/
└── <campaign-slug>/            e.g. youtube-collab-q2/
    ├── campaign.md             # the approved goal (this skill writes it)
    ├── leads.csv               # the lead list (user drops it here)
    ├── leads-spec.md           # per-lead dossiers + drafts (leads-research writes it)
    └── outbox/                 # drafts (leads-deliver writes it, if not sending via Gmail)
```
Slug the campaign (lowercase, hyphens). Create `lead-system/<campaign-slug>/` first.

## Workflow (find context → clarify offer → write campaign.md → approve)

### 1. Find the context
The offer is built from who the user is. Look for context in this order, and **stop at the first hit**:
1. A path the user gave you (`/leads-plan ./_context`, or a brand file).
2. A `_context/` folder at the project root (read `brand-context.md`, `brand-voice.md`,
   `ideal-viewer-profile.md` / ICP files if present).
3. A `BRAND.md` at the project root.
4. Nothing found → **ask one question**: *"Point me at your context — a folder, a brand file, or
   just tell me in a sentence who you are and what you offer."* Do not invent a brand.

Read what you find. Summarize back in 2–3 lines so the user can correct it.

### 2. Clarify the offer — ask at most 3 questions
Read `references/offer-framework.md`. Ask with `AskUserQuestion` (2–3 options each, best default
first). Three or fewer — the campaign must stay short:
1. **Who you're targeting** — the lead segment (e.g. "AI-automation YouTubers 50K–1M subs").
2. **The goal** — what a *win* is. This is flexible, not just selling:
   Sell · Partner/collab · Network · Guest/podcast swap · Hire · Just-reach-out. Pick one primary.
3. **The hook you lead with** — your single most credible, *verifiable* asset (a product, a number
   with a source, a shipped result). See the verifiability rule below.

### 3. Write campaign.md (short — this is a feature, not a draft)
Three sections only. Keep the whole file under ~40 lines. Use the template in
`references/offer-framework.md`. Cover exactly:
- **WHO WE ARE + WHAT WE OFFER** — one paragraph + a bullet list of *verifiable* assets (each with a
  source URL where it's a claim/number).
- **WHO WE'RE TARGETING** — the ICP in 2–4 bullets (segment, size, the pain we relieve, where they
  hang out).
- **THE GOAL + THE ANGLE** — the one win-condition, and the one-line angle every message bends toward.

### 4. The verifiability rule (carry it into research)
A claim in outreach that the prospect knows is wrong ends the conversation. So in `campaign.md`:
- Every **number or outcome** must have a **source URL**. No source → don't put it in the offer.
- Never attach a number from one entity to another (someone else's "$X/month" is not yours).
- Prefer assets that are independently checkable: live product URLs, repo star counts, public
  sub counts, a bio line on a real page.

Report any unverifiable claim you had to drop, in one line.

### 5. Approve
Show `campaign.md`. Ask: *"This is the north star for every message — approve, or what's off?"*
Once approved, point the user to `/leads-research <path-to-leads.csv>`.

## Output contract
- Writes `lead-system/<campaign-slug>/campaign.md` (short, 3 sections).
- Does NOT read or research any leads. Does NOT send anything.
