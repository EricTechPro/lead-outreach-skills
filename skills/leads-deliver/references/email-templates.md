# The canonical email template (v3 — peer networking)

**One template, used for every ✅ lead.** Personalization lives in the *words* (the two bullets and the
named niche), the look is uniform. Plain, personal, sent as HTML. Full style contract:
`references/email-style.md`. The rendered look the user approves before sending is the
`outbox/_preview.html` built by `scripts/build_previews.py` (see `references/preview-pages.md`).

All `{{tokens}}` are filled from `campaign.md`'s **Delivery style** block — never hardcode contact
values here.

## What the author writes (the draft body in leads-spec.md)

The draft is written in **plain text with markers** — the build step turns markers into HTML:
`**bold**` → `<strong>`, `==highlight==` → yellow `<mark>`, `- ` lines → `<ul><li>`. Write the body in
this exact 7-part order (greeting → intro → 2 bullets → bold reason → one ==highlight== invite → close →
signature).

### English skeleton
```
Hey {{first_name}},

I'm {{sender_first}} — I run {{channel_name}} ({{channel_url}}); we're in the same {{shared_niche}}
lane, so I wanted to reach out creator-to-creator.

A couple things:
- {{reciprocal_overlap — a topic/video THEY did + "I've made the same kind of thing"}}
- {{their_community_or_angle — from the research}}

**In this niche everyone's heads-down on their own track, and there's barely anywhere we actually talk
to each other.** ==I'm reaching out to creators in our space to connect — if you've already got a room
like that I'd love to join; if not, I'm building one and I'll loop you in.==

Either way, if you ever want to trade notes or have a question, I'm around. Open to connecting?

— {{sender_first}}
{{channel_name}} (YouTube) · {{youtube_handle}}
WhatsApp: {{whatsapp}}
```

### Chinese skeleton (whole email in Chinese — see language rule)
```
{{name}}你好！

我是 {{sender_first}}，做 {{channel_name}} 频道（{{channel_url}}），跟你一样在 {{shared_niche}}
这个方向做内容，以创作者的身份来打个招呼。

简单说两点：
- {{reciprocal_overlap — 他们做过的某个主题/视频 + “我自己也在做类似的”}}
- {{their_community_or_angle — 来自调研}}

**这个圈子里大家其实都在各做各的，平时几乎没什么交流。** ==我最近在联系一批同方向的创作者，想拉一个小群一起
交流什么内容有效、怎么变现——如果你已经有这样的群，我很想加入；如果还没有，我正在张罗，到时候把你也拉进来。==

有任何问题或者想交流随时找我。有兴趣的话回我一句就行 😄

—— {{sender_first}}
WhatsApp：{{whatsapp}} ｜ 微信 WeChat：{{wechat}} ｜ {{youtube_handle}}
```

## Marker → HTML (what the build step emits)
| Marker | HTML |
|---|---|
| blank line between blocks | `<p>…</p>` |
| single newline inside a block | `<br>` |
| consecutive `- ` lines | `<ul><li>…</li></ul>` |
| `**bold**` | `<strong>bold</strong>` |
| `==highlight==` (exactly one) | `<mark style="background:#fde047;padding:0 2px;border-radius:2px;">…</mark>` |
| `{{channel_url}}` / `{{youtube_handle}}` | the **only** `<a>` link |

The whole body renders inside one plain `<div>`:
`font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
font-size:15px;line-height:1.6;color:#222;` — **no card, no table wrapper, no accent rule, no image**.

---

## Worked example — ENGLISH (reproduce this exact look)
```
Subject: Fellow AI creator — same niche, saying hi 👋

Hey Zen,

I'm Eric — I run Eric Tech (https://www.youtube.com/@erictechpro); we're in the same local Claude Code /
AI-coding lane, so I wanted to reach out creator-to-creator.

A couple things:
- Saw you did the "AI Coding Without Rate Limits" local Claude Code video — I've made the same kind of
  thing, so we're clearly after the same audience
- And you built the AI Engineer Skool community around it, which is exactly the kind of space I'm after

**In this niche everyone's heads-down on their own track, and there's barely anywhere we actually talk to
each other.** ==I'm reaching out to creators in our space to connect — if you've already got a room like
that I'd love to join; if not, I'm building one and I'll loop you in.==

Either way, if you ever want to trade notes or have a question, I'm around. Open to connecting?

— Eric
Eric Tech (YouTube) · youtube.com/@erictechpro
WhatsApp: +1 555-867-5309
```

## Worked example — CHINESE (reproduce this exact look)
```
Subject: 同行 AI 创作者 — 打个招呼 👋

AI超元域你好！

我是 Eric，做 Eric Tech 频道（https://www.youtube.com/@erictechpro），跟你一样在 Claude Code / AI agent
这个方向做内容，以创作者的身份来打个招呼。

简单说两点：
- 看到你在 X 上分享 Claude Code 动态工作流生成的内容，我自己也在做类似的实战教程，咱们显然在追同一批受众
- 你还自己做了 Aila 这个多模型桌面工具，把 ChatGPT、Gemini、Claude 都整合进去

**这个圈子里大家其实都在各做各的，平时几乎没什么交流。** ==我最近在联系一批同方向的创作者，想拉一个小群一起
交流什么内容有效、怎么变现——如果你已经有这样的群，我很想加入；如果还没有，我正在张罗，到时候把你也拉进来。==

有任何问题或者想交流随时找我。有兴趣的话回我一句就行 😄

—— Eric
WhatsApp：+1 555-867-5309 ｜ 微信 WeChat：your_wechat_id ｜ youtube.com/@erictechpro
```

## Rules carried into every email
- Exactly **2 bullets**; **one** `**bold**` reason; **exactly one** `==highlight==` (the invite).
- **One link** (the channel) — in body and signature. No images, no tracking pixels, no attachments.
- **No view counts**, no "viral", no self-promotion by numbers. Lead with the niche.
- WhatsApp on every email; **WeChat only on Chinese** emails.
- Same template for everyone — vary the *words*, never the layout.

> Warm-list / newsletter layouts (header image, color blocks, button CTA) are **not** used for this
> campaign type — they hurt cold deliverability. The legacy branded showcase in
> `_templates/email/gallery.html` is kept only as a reference for opted-in warm lists.
