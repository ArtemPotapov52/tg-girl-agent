# girl-agent

Telegram AI persona engine with memory, schedule, relationship state, WebUI dashboard, and MTProto userbot mode.

## Features

- **Autonomous Telegram Persona**: Operates as a real Telegram user (via MTProto GramJS/Telegram client) with human-like typing delays, sleep schedules, and busy hours.
- **WebUI Dashboard**: Manage personas, conversation history, goals, schedule, voice settings, and live system logs via a modern web interface.
- **Long-Term Memory & Relationship System**: Tracks relationship stages, affection, trust, mutual context, and episodic memory.
- **Goals & Social Engineering Engine**: Customizable funnel / goals framework with soft mentions, qualification quizzes, and direct calls-to-action.
- **Voice Support**: TTS generation (Fish Audio / edge-tts) with procedural ambience and foley mixing (`voice_mix.py`) and Whisper STT transcription.
- **Safety & Anti-Loop Guards**: Built-in anti-nag, anti-repetition, spam/flood breaker, and silence recovery.

---

## Quick Start

### 1. Requirements

- Node.js >= 18.18
- Python 3.10+ (optional, for voice mixing and local Whisper)
- ffmpeg & ffprobe (optional, for voice processing)

### 2. Installation

```bash
git clone https://github.com/ArtemPotapov52/girl-agent.git
cd girl-agent
npm install
```

### 3. Configuration

Copy the deployment environment file:

```bash
cp deploy/girl-agent.env.example .env
```

Edit `.env` and set your credentials:
- `GIRL_AGENT_WEBUI_PASSWORD` — password to access the WebUI dashboard.
- `GROQ_API_KEY` / `FISH_API_KEY` — (optional) for fast STT and voice synthesis.

### 4. Running the WebUI

```bash
node dist/cli.js --port 3000 --host 0.0.0.0
```

Open `http://localhost:3000` in your browser and enter your admin password.

---

## Directory Structure

```
├── dist/                # Pre-built engine (cli.js and WebUI frontend)
├── data/                # Persona profiles, configuration, and state
│   └── марта/          # Starter persona profile
│       ├── config.json  # Persona Telegram & LLM settings
│       ├── persona.md   # Persona background & identity
│       ├── boundaries.md# Behavior boundaries
│       ├── speech.md    # Speech style & vocabulary
│       └── goals/       # Conversion & goals definitions
├── deploy/              # systemd unit & environment template
├── voice/               # Voice mixing & model download scripts
├── package.json
└── README.md
```

---

## Deploying with systemd (Linux VPS)

1. Copy the systemd service file:
   ```bash
   sudo cp deploy/girl-agent.service /etc/systemd/system/
   ```

2. Copy and configure the environment:
   ```bash
   sudo cp deploy/girl-agent.env.example /etc/girl-agent.env
   sudo nano /etc/girl-agent.env
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable girl-agent.service
   sudo systemctl start girl-agent.service
   ```

4. View logs:
   ```bash
   journalctl -u girl-agent.service -f
   ```

---

## License

See [LICENSE](LICENSE) file.
