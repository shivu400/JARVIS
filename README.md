# J.A.R.V.I.S Personal AI Assistant

A voice-controlled personal AI assistant inspired by JARVIS from Iron Man, built using Python and open-source libraries.

## Features

- **Voice Input**: Listens for voice commands using speech recognition
- **Voice Output**: Responds with natural-sounding speech
- **Wake Word Detection**: Activates when you say "Jarvis"
- **Smart Responses**: Uses pre-defined responses and Wikipedia for information
- **GUI Interface**: Clean, modern interface with visual feedback
- **Task Execution**:
  - Tell time and date
  - Check weather using free wttr.in API
  - Open websites
  - Search Wikipedia
  - Answer basic questions
  - Tell jokes

## Requirements

- Python 3.7+
- Microphone
- Speakers
- Internet connection

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/jarvis.git
cd jarvis
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Generate the JARVIS icon (optional):
```
python create_icon.py
```

## Usage

Run the launcher script which will guide you through starting JARVIS:
```
python run_jarvis.py
```

You can also directly specify the mode:
```
python run_jarvis.py --cli  # Command-line interface
python run_jarvis.py --gui  # Graphical user interface
```

### Command-Line Mode

1. Run the CLI version:
```
python jarvis.py
```

2. Say "Jarvis" to activate the assistant
3. Speak your command or question after the greeting

### GUI Mode

1. Run the GUI version:
```
python jarvis_gui.py
```

2. The interface will show the status and conversation history
3. Say "Jarvis" to activate or click the "Listen" button

## Example Commands

- "What time is it?"
- "What's the weather in New York?"
- "Open youtube.com"
- "Tell me about artificial intelligence"
- "Tell me a joke"
- "Goodbye" (puts JARVIS back to sleep)
- "Exit" (terminates the program)

## Free APIs Used

Instead of requiring API keys, this version of JARVIS uses free alternatives:

- **Weather Information**: wttr.in API (no key required)
- **Knowledge Base**: Wikipedia and pre-defined responses
- **Speech Recognition**: Google Speech Recognition API (free tier)

## Customization

You can customize JARVIS by:

- Changing the wake word in `jarvis.py`
- Adding new responses in the `ai_responses` dictionary
- Adding new commands in the `execute_command` method
- Adjusting speech settings (voice, rate) in the initialization
- Modifying the GUI appearance in `jarvis_gui.py`

## Troubleshooting

- If you encounter issues with PyAudio installation on Windows, try:
```
pip install pipwin
pipwin install pyaudio
```

- For Linux, you may need to install portaudio:
```
sudo apt-get install python3-pyaudio
```

- For macOS, you may need to install portaudio:
```
brew install portaudio
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 