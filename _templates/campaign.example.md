# Campaign: YouTube collab Q2

## Who we are + what we offer
Eric Tech — ex-Microsoft & Amazon senior engineer who ships real AI products and teaches the
engineering behind them. The lane: Claude Code, MCP servers, agent frameworks, and shipping AI SaaS.

**Verifiable assets** (every claim has a source — no source, no claim):
- BookZero — live AI bookkeeping SaaS, $14/mo, Gemini OCR → bank matching → QuickBooks — https://www.bookzero.ai
- `startup-claude-skills` — 48★ — https://github.com/EricTechPro/startup-claude-skills
- `awesome-claude-code-agents` — 78★ — https://github.com/EricTechPro/awesome-claude-code-agents
- Eric Tech — 61.7K subs, +6.6K/30d — https://www.youtube.com/@ericwtech (src: vidiq)

## Who we're targeting
- Segment: AI-automation / Claude Code YouTubers, 50K–1M subs
- Size / signal: active channel, audience overlaps ours but leans no-code (complementary)
- Their pain we relieve: their audience wants the technical depth they don't go deep on
- Where they are: YouTube, Skool communities, X

## The goal + the angle
- **Goal (one win):** Guest / podcast swap (peer collab)
- **The angle:** "your audience learns to *sell* AI; I show them how to *ship* it" — complementary, not competitive
- **The ask (lowest-effort next step):** "worth a 15-min call?" / "episode + cross-share?"

## Delivery style
How `leads-research` drafts and `leads-deliver` renders/sends every email. The skills read these keys —
**nothing about the look or the contact values is hardcoded in the skills.** (Style spec:
`skills/leads-deliver/references/email-style.md`.)

```yaml
# --- format -------------------------------------------------------------
format: HTML, plain/personal       # reads like a normal person typed it in Gmail — NOT a newsletter

# --- typography ---------------------------------------------------------
typography:
  font: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
  body: 15px
  line_height: 1.6
  color: "#222"
  emphasis: bold + one yellow highlight
  highlight_hex: "#fde047"
  links: 1                          # the YouTube channel only — no images, no tracking

# --- the 7-part structure (in order) ------------------------------------
email_structure:
  1: greeting with their name           # "Hey <First>,"  ·  Chinese: "<name>你好！"
  2: one intro line                     # who you are + channel link + NAMED shared niche (no stats)
  3: exactly 2 bullets                  # 1) reciprocal overlap (a video THEY did + "I've done the same")
                                        # 2) their community / their angle   — NO view counts
  4: the strong reason in **bold**      # niche is small, everyone heads-down, nowhere creators talk
  5: the invite in ONE ==highlight==    # group chat to learn/share — join-or-build
  6: welcoming close + one light ask    # "trade notes anytime — open to connecting?"
  7: signature                          # see contact

# --- subject (peer intro, never the topic) ------------------------------
subject:
  style: peer/colleague introduction    # topic/keyword subjects get filtered — forbidden
  prefix_en: "Fellow AI creator"         # searchable constant prefix + short varied tail
  prefix_zh: "同行 AI 创作者"
  # tail rotates: "👋" · "— same niche, saying hi 👋" · "— builder in your lane 👋" · "— 打个招呼 👋"

# --- contact (fill with YOUR values; sent to leads) ---------------------
contact:
  channel_name: "Eric Tech"
  channel_url: "https://www.youtube.com/@erictechpro"
  youtube_handle: "youtube.com/@erictechpro"   # bare display form in the signature
  sign_off_en: "— Eric"
  sign_off_zh: "—— Eric"
  whatsapp: "+1 555-867-5309"     # ← your WhatsApp — on EVERY email          (placeholder: replace)
  wechat: "your_wechat_id"        # ← your WeChat — CHINESE emails only        (placeholder: replace)

# --- language -----------------------------------------------------------
language_rule: >
  Write the whole email in Chinese if the channel name/handle has Chinese characters OR the research
  says a Chinese-language audience; otherwise English. Bullets/bold/highlight all match the language.

# --- hard rule ----------------------------------------------------------
hard_rule: >
  Never mention our own view counts or viral/trending videos — and never cite "X views" for anyone.
  Lead with the niche, not numbers. Always reciprocal framing. One link (the channel) only.
```

> The `whatsapp` and `wechat` above are **placeholders** — replace with your own before a real run.
> They're kept generic so anyone cloning this repo doesn't ship someone else's contact details.
