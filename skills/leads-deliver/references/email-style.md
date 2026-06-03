# Email style & format (v3 — peer networking)

The `leads-spec.md` defines *what* each message says. This defines *how it looks and reads* when
delivered. There is **one canonical style** for this campaign type — a plain, personal, creator-to-creator
note. It is sent as HTML (so bullets/bold/highlight survive an HTML send node) but must read like a
normal person typed it in Gmail. Not a newsletter.

> The single fill-in template + worked examples live in `references/email-templates.md`. The three
> rendered preview artifacts (what the user eyeballs before the send gate) live in
> `references/preview-pages.md`. This file is the **style contract** those follow.

All concrete values (channel link, WhatsApp, WeChat, subject prefixes, sign-off) come from
`campaign.md`'s **Delivery style** block — never hardcode them here. Tokens below in `{{double_braces}}`
are filled from that block.

## Format — plain, personal, HTML (NOT a newsletter)
- **System font stack only:**
  `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`.
- Body **15px**, line-height **1.6**, color **#222**.
- **NO** card/table wrapper, **NO** colored rule, **NO** brand accent color, **NO** header/logo image,
  **NO** tracking pixels.
- **One link max** — the YouTube channel ({{channel_url}}). Bullets are real `<ul><li>`.
- Emphasis: **bold** for the ONE strong reason; exactly **one** yellow highlight ({{highlight_hex}},
  default `#fde047`) on the invite line. Nothing else is colored.

## The 7-part structure — every email, in this order
1. **Greeting with their name** — `Hey <FirstName>,`. A brand/team channel → the brand name or the
   founders' names. Chinese → `<name>你好！`.
2. **One intro line** — who you are + the channel link + the **named shared niche**. No numbers/stats.
   e.g. *"I'm {{sender_first}} — I run {{channel_name}} ({{channel_url}}); we're in the same AI-coding
   lane, so I wanted to reach out creator-to-creator."*
3. **Exactly 2 bullets** (real `<ul><li>`):
   - **bullet 1 = reciprocal overlap** — reference a topic/video **they** did and say you've made the
     same kind of thing ("saw you did X — I've done the same kind of thing").
   - **bullet 2 = their community / their angle** — from the research (their Skool/Discord, their tool,
     their format).
   - **No view counts.**
4. **The strong reason in bold** — the niche is small and everyone is heads-down on their own track,
   with barely anywhere creators actually talk to each other.
5. **The invite in ONE yellow highlight** — you're connecting creators in the niche into a group chat to
   learn/share. **Join-or-build:** if they already have a room, ask to join; if not, you're
   building/finding one and will loop them in.
6. **Welcoming close + one light ask** — *"if you ever want to trade notes or have a question, I'm
   around. Open to connecting?"*
7. **Signature** — plain lines (see below).

## Hard rules
- **Never** mention our own viral/trending videos or **any** view counts (no "243K", no "blew up").
  Lead with the niche, not numbers. Do not cite "X views" for **anyone** — them or us.
- **Always reciprocal framing** — "saw you did X — I've made the same kind of thing."
- **Always name the shared niche explicitly** — AI coding / Claude Code / n8n automation / AI agents,
  whichever fits the lead.
- **One link only** (the YouTube channel). No images, no tracking.

## Emphasis markers (authors write these in the draft; the build step converts them)
| In the draft text | Rendered HTML |
|---|---|
| `**bold**` | `<strong>bold</strong>` |
| `==highlight==` | `<mark style="background:#fde047;padding:0 2px;border-radius:2px;">highlight</mark>` |

Exactly **one** highlight per email (the invite line). Multiple bolds are fine but keep the bold for the
ONE strong reason.

## Signature (values from campaign.md — placeholders only here)
**English:**
```
— {{sender_first}}
{{channel_name}} (YouTube) · {{youtube_handle}}
WhatsApp: {{whatsapp}}
```
**Chinese:**
```
—— {{sender_first}}
WhatsApp：{{whatsapp}} ｜ 微信 WeChat：{{wechat}} ｜ {{youtube_handle}}
```
- **WhatsApp on every email. WeChat only on Chinese emails.** Channel link in the body **and** the
  signature.

## Language rule
Write the **whole** email in natural Chinese if the channel's name/handle contains Chinese characters
**OR** the research says it's a Chinese-language channel/audience. Otherwise English. In Chinese emails
the bullets, bold, and highlight are all Chinese too — not a translated English skeleton.

## Subject lines — a peer INTRODUCTION, never the topic
- A colleague intro, **never** the topic. Topic/keyword subjects (e.g. "Claude Code + n8n") get
  filtered out — **forbidden**.
- **Searchable constant prefix + short varied tail**, so the whole campaign is findable in Sent.
  - English prefix: **{{en_subject_prefix}}** (default `Fellow AI creator`)
  - Chinese prefix: **{{zh_subject_prefix}}** (default `同行 AI 创作者`)
- Rotate the tail for variety:
  - EN: `Fellow AI creator 👋` · `Fellow AI creator — YouTuber to YouTuber 👋` ·
    `Fellow AI creator — same niche, saying hi 👋` · `Fellow AI creator — builder in your lane 👋`
  - ZH: `同行 AI 创作者 👋` · `同行 AI 创作者 — 打个招呼 👋` · `同行 AI 创作者 — 交个朋友 👋`

## Why this style (deliverability + reply rate)
Plain, personal, one-link mail reads as 1:1 human mail, lands in the inbox (not Promotions), and gets
the highest reply rates for cold creator-to-creator outreach. The HTML send node is only there so
bullets/bold/the single highlight render — it is **not** a newsletter wrapper. Branded/newsletter
layouts (header images, color blocks, multi-link footers) hurt cold deliverability and are not used for
this campaign type.
