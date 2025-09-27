# Jarvis Voice Assistant

Jarvis is a Python-based voice assistant that can:
- Recognize wake words and commands using your microphone
- Speak responses using gTTS and pyttsx3
- Open websites and search Google or YouTube for queries
- Play music from a local library or search YouTube
- Fetch and read news headlines using NewsAPI
- Respond to general queries with OpenAI (if API key is provided)

## Features
- Wake word detection ("Jarvis")
- Voice command processing for web, music, news, and more
- Automatic fallback to Google or YouTube search for unknown commands
- News headlines for US or topic-based news
- Interrupt news reading by saying "stop"

## Setup
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your NewsAPI and OpenAI API keys in `main.py`.
4. Run the assistant:
   ```bash
   python main.py
   ```

## Requirements
- Python 3.7+
- `speech_recognition`, `pyttsx3`, `gtts`, `pygame`, `requests`, `musiclibrary` (custom)

## Usage
- Say "Jarvis" to activate.
- Give commands like:
  - "open Google"
  - "play [song name]"
  - "news" or "news about [topic]"
  - "search [topic]"
  - "stop" (to interrupt news)

## Notes
- For OpenAI features, you need a valid API key and quota.
- For NewsAPI, you need a valid API key.
- Music library is defined in `musiclibrary.py`.

## License
MIT

---
Made with ❤️ by AshuferMorningstar
