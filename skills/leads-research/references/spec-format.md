# leads-spec.md format

One file per campaign. **One section per lead.** Built to be *skimmed*: the verdict is the heading,
so the user scrolls and instantly sees who to contact. Never edit the CSV — this `.md` is the
review surface (plan-before-send, like a spec).

## File header

```markdown
# Leads — <campaign name>

Goal: <one line from campaign.md>  ·  Researched: <N> leads  ·  ✅ <a>  🟡 <b>  ❌ <c>  ⚠️ <d not researched>

> Review the ✅ sections. Edit any draft inline. When happy, run `/leads-deliver`.
```

## Per-lead section — the pyramid (WHO → FIT → SEND)

The verdict emoji is in the **heading** so the eye lands on it first. Three layers, top-down: who
they are → whether/why they fit → the message. Use **bold labels**, not `===` rules.

```markdown
### ✅ <Name> — <Strong fit · recommend>

**WHO** — <one line: who they are> <then a little deeper: size/role/what they're known for>.
<key stats with sources, e.g.> 782K subs, +77K/30d (src: vidiq). Founder of Uppit AI (src: nateherk.com).

**FIT** — ✅ **Why:** <reason grounded in the research — the specific overlap with the campaign goal>.
**Hook:** <the one concrete thing to open with — a shared topic, a complementary audience, a named
asset of theirs>. <If 🟡, say what's uncertain. If ❌, say why and stop — no draft.>

**SEND** — *(drafted with the copywriting rules)*
**Subject:** <≤6 words, specific>
<short personalized body — 3–5 lines, references something real from WHO/FIT, one ask matched to the goal>
```

## Rules

- **Heading verdict** — `✅ recommend` / `🟡 borderline` / `❌ skip` / `⚠️ not researched`. Sort or
  group ✅ first if the list is long, so the user reviews the actionable ones up top.
- **Source-attributed** — every number/claim in WHO/FIT carries an inline `(src: <url>)`. A claim
  with no source is dropped, or marked `⚠️ unverified — <where it came from>`.
- **No draft for ❌.** Skips don't get a message. `🟡` gets a draft only if the user opts in.
- **SEND is short and real** — personalized from the research, not a template with the name swapped.
  No revenue/claim about the lead unless it's sourced in WHO.
- **One ask** — matched to the campaign goal (call / reply / collab / podcast). Lowest-effort step.
- **Editable** — the user can rewrite any draft directly in the file; `/leads-deliver` reads what's
  there at send time.

## Worked example (real data)

```markdown
### ✅ Nate Herk — Strong fit · recommend

**WHO** — Nate Herk, AI Automation Creator & Educator, founder of Uppit AI (src: nateherk.com).
782K subs, +77K/30d — fast-growing (src: vidiq). Teaches building & selling AI agents with n8n +
Claude Code; top videos are monetization-led ("Build & Sell with Claude Code", "$100M AI Agency")
(src: vidiq top videos). Collabs run through his AI Automation Society Podcast (src: youtube playlist).

**FIT** — ✅ **Why:** complementary, not competitive — his audience is no-code "build & sell"; ours
is the technical depth behind shipped products. Goal = guest/podcast swap.
**Hook:** his podcast format (guest + concrete framework) ↔ our shipped AI SaaS + open-source skills.

**SEND**
**Subject:** built a real AI SaaS with Claude Code
Nate — your audience learns to sell AI; mine is the engineers who ship it. I built BookZero (live AI
bookkeeping app: Gemini OCR → bank matching → QuickBooks) and open-source the Claude Code skills I
run the startup on (48★ + 78★ repos). That's an episode for the AI Automation Society Podcast —
concrete framework + a free template for your people, and I'll cross-share to my dev audience. 15 min?
```
