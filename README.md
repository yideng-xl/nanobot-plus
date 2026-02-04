<div align="center">
  <h1>🚀 nanobot-plus</h1>
  <p><strong>Enhanced fork of <a href="https://github.com/HKUDS/nanobot">HKUDS/nanobot</a> with extended platform support</strong></p>
  <p>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <img src="https://img.shields.io/badge/upstream-HKUDS%2Fnanobot-orange" alt="Upstream">
  </p>
</div>

## 🎯 What is nanobot-plus?

**nanobot-plus** is a community-maintained fork of the excellent [nanobot](https://github.com/HKUDS/nanobot) project from Hong Kong University's Data Intelligence Lab (HKUDS).

We extend the original ultra-lightweight AI assistant (~4,000 lines of code) with **additional platform integrations** and **enhanced features** while staying synchronized with upstream updates.

### Relationship with HKUDS/nanobot

| Aspect | HKUDS/nanobot | nanobot-plus |
|--------|---------------|--------------|
| **Maintainer** | HKU Data Intelligence Lab | Community (yideng-xl) |
| **Focus** | Core functionality, research | Extended integrations |
| **Channels** | Telegram, WhatsApp | Telegram, WhatsApp, **Feishu/Lark** |
| **Updates** | Official releases | Synced with upstream + enhancements |

We regularly pull from upstream to ensure you get the latest official improvements plus our additional features.

---

## ✨ Plus Features

Features added in nanobot-plus beyond the original:

| Feature | Status | Description |
|---------|--------|-------------|
| 🪶 **Feishu/Lark Channel** | ✅ Ready | Native long-connection support for Feishu (飞书) |
| 🔒 **Allowlist Security** | ✅ Ready | Restrict bot access to specific users |
| 🤖 **Gemini Integration** | ✅ Ready | Pre-configured for Google Gemini models |
| 🏎️ **NVIDIA NIM Support** | ✅ Ready | Integrated support for NVIDIA Inference Microservices |

---

## 📦 Install

```bash
git clone https://github.com/yideng-xl/nanobot-plus.git
cd nanobot-plus
pip install -e .
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv venv && source .venv/bin/activate
uv pip install -e .
```

## 🚀 Quick Start

**1. Initialize**

```bash
nanobot onboard
```

**2. Configure** (`~/.nanobot/config.json`)

```json
{
  "providers": {
    "gemini": {
      "apiKey": "YOUR_GEMINI_API_KEY"
    }
  },
  "agents": {
    "defaults": {
      "model": "gemini/gemini-2.0-flash"
    }
  }
}
```

**3. Chat**

```bash
nanobot agent -m "你好！"
```

---

## 💬 Chat Apps

Talk to your nanobot through multiple platforms.

| Channel | Setup | Status |
|---------|-------|--------|
| **Telegram** | Easy (just a token) | ✅ Original |
| **WhatsApp** | Medium (scan QR) | ✅ Original |
| **Feishu/Lark** | Easy (App ID + Secret) | ✅ **Plus Feature** |

<details>
<summary><b>Telegram</b></summary>

**1. Create a bot**
- Open Telegram, search `@BotFather`
- Send `/newbot`, follow prompts
- Copy the token

**2. Configure**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

**3. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>WhatsApp</b></summary>

Requires **Node.js ≥18**.

**1. Link device**

```bash
nanobot channels login
```

**2. Configure**

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+1234567890"]
    }
  }
}
```

**3. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Feishu/Lark (飞书)</b> ⭐ Plus Feature</summary>

Works behind NAT/firewalls — no public IP required!

**1. Create a Feishu App**
- Go to [Feishu Open Platform](https://open.feishu.cn)
- Create a self-built app
- Enable bot capability
- Add event subscription: `im.message.receive_v1`
- Set connection mode to **Long Connection (长连接)**

**2. Configure**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "app_id": "cli_xxxxx",
      "app_secret": "your_app_secret",
      "allow_from": ["ou_xxxxx"]
    }
  }
}
```

**3. Run**

```bash
nanobot gateway
```

</details>

---

## ⚙️ Configuration

Config file: `~/.nanobot/config.json`

### Providers

| Provider | Purpose | Get API Key |
|----------|---------|-------------|
| `openrouter` | LLM (access to all models) | [openrouter.ai](https://openrouter.ai) |
| `anthropic` | LLM (Claude direct) | [console.anthropic.com](https://console.anthropic.com) |
| `openai` | LLM (GPT direct) | [platform.openai.com](https://platform.openai.com) |
| `gemini` | LLM (Gemini direct) | [aistudio.google.com](https://aistudio.google.com) |
| `groq` | LLM + Voice transcription | [console.groq.com](https://console.groq.com) |

<details>
<summary><b>Full config example</b></summary>

```json
{
  "agents": {
    "defaults": {
      "model": "gemini/gemini-2.0-flash"
    }
  },
  "providers": {
    "gemini": {
      "apiKey": "AIza..."
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "app_id": "cli_xxxxx",
      "app_secret": "secret",
      "allow_from": ["ou_xxxxx"]
    },
    "telegram": {
      "enabled": false
    },
    "whatsapp": {
      "enabled": false
    }
  }
}
```

</details>

---

## 📁 Project Structure

```
nanobot/
├── agent/          # 🧠 Core agent logic
├── channels/       # 📱 Platform integrations (Telegram, WhatsApp, Feishu)
├── providers/      # 🤖 LLM providers
├── skills/         # 🎯 Bundled skills
├── bus/            # 🚌 Message routing
├── cron/           # ⏰ Scheduled tasks
├── session/        # 💬 Conversation sessions
└── cli/            # 🖥️ Commands
```

---

## 🤝 Contributing

PRs welcome! We're especially interested in:

- [ ] **More channels** — Discord, Slack, DingTalk, WeChat Work
- [ ] **Rich message support** — Feishu cards, interactive buttons
- [ ] **Document tools** — Read/write Feishu Docs, Wiki, Bitable
- [ ] **Voice support** — Speech-to-text for Feishu

---

## ⭐ Star History

<div align="center">
  <a href="https://star-history.com/#yideng-xl/nanobot-plus&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=yideng-xl/nanobot-plus&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=yideng-xl/nanobot-plus&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=yideng-xl/nanobot-plus&type=Date" />
    </picture>
  </a>
</div>

---

## 🙏 Acknowledgments

- **[HKUDS/nanobot](https://github.com/HKUDS/nanobot)** — The brilliant original project from Hong Kong University
- **[OpenClaw](https://github.com/openclaw/openclaw)** — Inspiration for the personal AI assistant concept

---

<p align="center">
  <sub>nanobot-plus is for educational, research, and personal use.</sub>
</p>
