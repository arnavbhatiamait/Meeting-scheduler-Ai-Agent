# Meeting Scheduler AI Agent

A smart, cross-platform AI agent that schedules meetings, manages tasks, and answers questions from meeting transcripts using natural language via chat or voice. Works through a Telegram bot today, with WhatsApp support in progress.

- Repository: arnavbhatiamait/Meeting-scheduler-Ai-Agent

## Highlights

- Schedules Google Meet meetings and returns join links from natural requests
- Adds and manages tasks via Todoist
- Memory-based Q&A over meeting transcripts: ask what was discussed or decided
- Accepts voice or text input; live interaction through Telegram
- LLM-agnostic: OpenAI, Groq, Gemini, or local Ollama

## Demo Screenshots
![img1](https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent/blob/main/WhatsApp%20Image%202025-05-06%20at%2014.57.04_7e67010d.jpg)
![img2](https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent/blob/main/WhatsApp%20Image%202025-05-06%20at%2014.57.07_1be6ecec.jpg)
![img3](https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent/blob/main/WhatsApp%20Image%202025-05-06%20at%2014.57.17_40b8738a.jpg)
![img4](https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent/blob/main/WhatsApp%20Image%202025-05-06%20at%2014.57.46_7860bdce.jpg)
![img5](https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent/blob/main/WhatsApp%20Image%202025-05-06%20at%2014.57.46_f8caa869.jpg)
![img6](https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent/blob/main/WhatsApp%20Image%202025-05-06%20at%2014.57.47_2a6069f0.jpg)
![img7](https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent/blob/main/WhatsApp%20Image%202025-05-06%20at%2014.58.10_63527c1c.jpg)
Example embeds:

- Schedule meetings:
  - “Schedule a Google Meet with the design team tomorrow at 3pm IST. Agenda: UI review.”
- Manage tasks:
  - “Add Todoist task: Send follow-up notes to team, due Friday.”
- Meeting intelligence:
  - “What did we decide in yesterday’s sprint planning?”
  - “Summarize action items from the last two meetings.”
- Voice input:
  - Use speech recognition to issue commands hands-free.
- Chat agents:
  - Telegram bot for real-time interaction (WhatsApp in development).

## Key Features

- LLM choice: OpenAI, Groq, Gemini, Ollama
- Google Meet integration: Create events, fetch links/metadata via Google Calendar API
- Transcript analysis: Parse and summarize meeting transcripts; extract decisions and action items
- Memory-based Q&A: Natural-language questions over past meetings
- Todoist API: Create and organize tasks/projects
- Telegram Bot: Production-ready chat interface
- Voice support: Speech recognition for commands

## Tech Stack

- Python, Streamlit — app logic and UI
- LLMs — OpenAI, Groq, Gemini, Ollama
- Google Calendar API — schedules meetings, fetches Meet links
- Todoist API — task management
- Transcript Parser — summarization and Q&A grounding
- Telegram Bot API — chat interface
- Speech Recognition — voice input

## Project Structure

- app.py — Streamlit entry point and UI
- all_classses.py — agent logic, tools, and service wrappers (LLMs, Google, Todoist, Telegram, transcripts, speech)
- project_all_classes.ipynb — notebook for development/experiments
- requirements.txt — Python dependencies
- images/ — screenshots for README (add PNG/JPG files here)
- data/ or samples/ — example transcript files (optional)

## Getting Started

1) Clone and set up environment
- git clone https://github.com/arnavbhatiamait/Meeting-scheduler-Ai-Agent.git
- cd Meeting-scheduler-Ai-Agent
- python -m venv .venv
- source .venv/bin/activate  (Windows: .venv\Scripts\activate)
- pip install -r requirements.txt

2) Environment variables (.env)
- MODEL_PROVIDER=openai|groq|gemini|ollama
- MODEL_NAME=gpt-4o|llama3|gemini-1.5|...
- OPENAI_API_KEY=...
- GROQ_API_KEY=...
- GEMINI_API_KEY=...
- OLLAMA_BASE_URL=http://localhost:11434
- TODOIST_API_TOKEN=...
- TELEGRAM_BOT_TOKEN=...
- GOOGLE_API_CREDENTIALS=/absolute/path/to/client_secret.json

3) Google OAuth (Calendar/Meet)
- Create a Google Cloud project; enable Google Calendar API
- Create OAuth 2.0 credentials; download client_secret.json
- Set GOOGLE_API_CREDENTIALS to the file path (or securely load the JSON)
- On first run, complete OAuth consent to store tokens locally

4) Todoist setup
- Create a Todoist API token; set TODOIST_API_TOKEN

5) Telegram bot
- Create a bot via @BotFather; set TELEGRAM_BOT_TOKEN
- Use webhook or long polling during development

6) Run
- streamlit run app.py
- Follow prompts; complete Google OAuth when requested

## Usage Examples

- Schedule a meeting:
  - “Set a Google Meet with Priya and Arjun on Wednesday 2–3pm, agenda: roadmap sync.”
- Task management:
  - “Add a Todoist task ‘Prepare slides for demo’, due tomorrow.”
- Transcript Q&A:
  - “What were the action items from last sprint review?”
  - “Who owns API documentation updates?”
- Voice:
  - Use the mic button (if available) to speak the command.

## How It Works

- Intent parsing: An LLM classifies user intent (schedule, tasks, Q&A)
- Tool use:
  - Google Calendar API creates events and fetches Meet links
  - Todoist API manages tasks and projects
  - Transcript pipeline summarizes meetings and powers follow-up Q&A
- Memory:
  - Structured summaries and metadata enable conversational queries over past meetings
- Multimodal:
  - Text or voice input; responses grounded in transcripts when applicable

## Security & Privacy

- Store OAuth tokens and API keys securely; never commit .env
- Review data retention for transcripts and logs in production
- Follow least-privilege principles for OAuth scopes

## Roadmap

- WhatsApp integration
- Multi-calendar support and attendee availability checks
- Auto-generated minutes, agenda, and follow-up emails
- Vector memory for long-term transcript grounding
- Multi-user access control and roles
- Docker and one-click deploy

## Troubleshooting

- Google OAuth errors:
  - Verify credentials, scopes, and redirect URIs; re-run consent flow
- Telegram bot not responding:
  - Check token, webhook URL, and network/firewall
- LLM provider errors:
  - Validate MODEL_PROVIDER/MODEL_NAME and API keys
- Todoist issues:
  - Confirm token and project IDs; inspect API response logs
- Voice input:
  - Check microphone permissions and browser compatibility

## Contributing

Contributions are welcome. Open an issue for feature requests or bug reports. Submit PRs with clear descriptions and testing notes.

