import os
import time
import datetime
import random
import webbrowser
import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Default voice
engine.setProperty('rate', 180)  # Speed of speech

# Initialize Speech Recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Adjust for ambient noise
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)

# Wake word
WAKE_WORD = "jarvis"

# Personality responses
greetings = [
    "Hello sir. How may I assist you today?",
    "At your service, sir.",
    "JARVIS online. What can I do for you?",
    "Good day, sir. How can I help?",
    "Systems operational. Ready for your command."
]

acknowledgements = [
    "Right away, sir.",
    "Consider it done.",
    "I'm on it.",
    "Processing your request.",
    "As you wish."
]

farewell_responses = [
    "Goodbye, sir. Have a productive day.",
    "Going offline now. Call me when you need assistance.",
    "System shutting down. Until next time, sir.",
    "I'll be here when you need me. Goodbye."
]

confusion_responses = [
    "I didn't quite catch that. Could you repeat, sir?",
    "My apologies, but I didn't understand. Could you rephrase?",
    "I'm having trouble processing that command. Can you try again?",
    "That input is outside my parameters. Could you clarify?"
]

# Free AI responses for common queries
ai_responses = {
    "hello": ["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Greetings! How may I help you?"],
    "how are you": ["I'm functioning optimally, thank you for asking.", "All systems operational and ready to assist you.", "I'm doing well, ready to help with whatever you need."],
    "who are you": ["I am JARVIS, your personal AI assistant.", "I'm JARVIS, inspired by Tony Stark's AI. I'm here to assist you with various tasks.", "I'm your personal assistant JARVIS, ready to help with information and tasks."],
    "what can you do": ["I can tell time, search Wikipedia, open websites, provide information about various topics, and more.", "I can assist with telling the time, searching for information, opening websites, and answering questions.", "My capabilities include providing the time, searching Wikipedia, opening websites, and answering general questions."],
    "thanks": ["You're welcome, sir.", "Happy to assist.", "Anytime, sir.", "My pleasure."],
    "joke": ["Why don't scientists trust atoms? Because they make up everything.", "What did the ocean say to the beach? Nothing, it just waved.", "Why did the scarecrow win an award? Because he was outstanding in his field."],
}

class JarvisAssistant:
    def __init__(self):
        self.is_active = True
        self.is_listening = False
        print("Initializing JARVIS...")
        self.speak("JARVIS system initializing. All systems operational.")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"JARVIS: {text}")
        engine.say(text)
        engine.runAndWait()
    
    def listen(self):
        """Listen for user's voice input and convert to text"""
        with microphone as source:
            print("Listening...")
            audio = recognizer.listen(source)
            
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio).lower()
            print(f"User: {query}")
            return query
        except sr.UnknownValueError:
            self.speak(random.choice(confusion_responses))
            return ""
        except sr.RequestError:
            self.speak("I'm having trouble accessing the speech recognition service.")
            return ""
    
    def wait_for_wake_word(self):
        """Listen continuously for wake word"""
        print("Waiting for wake word...")
        with microphone as source:
            while not self.is_listening:
                try:
                    audio = recognizer.listen(source, timeout=1)
                    query = recognizer.recognize_google(audio).lower()
                    if WAKE_WORD in query:
                        self.speak(random.choice(greetings))
                        self.is_listening = True
                        return True
                except (sr.UnknownValueError, sr.WaitTimeoutError):
                    pass
                except sr.RequestError:
                    print("Could not access Google Speech Recognition service. Check your internet connection.")
                    time.sleep(5)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(1)
    
    def get_time(self):
        """Return the current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    
    def get_date(self):
        """Return the current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."
    
    def get_weather(self, city="London"):
        """Get weather information using a free weather API"""
        try:
            # Using wttr.in free weather API
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url)
            data = response.json()
            
            # Extract weather information
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            
            return f"The weather in {city} is {desc}. The temperature is {temp_c}°C with {humidity}% humidity."
        except Exception as e:
            return f"I encountered an error getting weather data: {e}"
    
    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            self.speak(f"Searching Wikipedia for {query}...")
            results = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {results}"
        except Exception as e:
            return f"I couldn't find that information on Wikipedia: {e}"
    
    def open_website(self, url):
        """Open a website in the default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            return f"Opening {url}"
        except Exception as e:
            return f"I couldn't open that website: {e}"
    
    def get_ai_response(self, query):
        """Generate a response based on pre-defined answers or rules"""
        # Check for exact matches in our AI responses dictionary
        for key, responses in ai_responses.items():
            if key in query:
                return random.choice(responses)
        
        # Check for general questions and provide canned responses
        if "what is" in query or "who is" in query or "how to" in query:
            return f"I suggest searching for information about '{query}' on Wikipedia or the web. Would you like me to search Wikipedia for you?"
        
        if "can you" in query:
            return "I can tell time, search Wikipedia, open websites, and have simple conversations. My capabilities are limited without external APIs, but I'm happy to help with what I can."
        
        # Default response if no rules match
        return "I'm not sure how to respond to that. I'm currently operating with limited capabilities as I'm not connected to advanced AI services."
    
    def search_free_answer(self, query):
        """Search for answers using free services"""
        # First try Wikipedia
        try:
            results = wikipedia.summary(query, sentences=1)
            return f"According to Wikipedia: {results}"
        except:
            pass
        
        # Then try a simple rule-based response
        return self.get_ai_response(query)
    
    def execute_command(self, query):
        """Execute a command based on the query"""
        # Time queries
        if "time" in query:
            return self.get_time()
        
        # Date queries
        elif "date" in query or "day" in query:
            return self.get_date()
        
        # Weather queries
        elif "weather" in query:
            city = "London"  # Default city
            words = query.split()
            for i, word in enumerate(words):
                if word in ["in", "at", "for"]:
                    if i + 1 < len(words):
                        city = words[i + 1]
            return self.get_weather(city)
        
        # Wikipedia queries
        elif "wikipedia" in query or "search for" in query or "tell me about" in query:
            search_term = query.replace("wikipedia", "").replace("search for", "").replace("tell me about", "").strip()
            return self.search_wikipedia(search_term)
        
        # Open website
        elif "open" in query and ("website" in query or "site" in query or ".com" in query or ".org" in query or ".net" in query):
            words = query.split()
            for word in words:
                if "." in word:
                    return self.open_website(word)
            return "I'm not sure which website to open."
        
        # Jokes
        elif "joke" in query or "funny" in query:
            return random.choice(ai_responses["joke"])
        
        # Goodbye
        elif "goodbye" in query or "bye" in query or "shutdown" in query or "shut down" in query:
            response = random.choice(farewell_responses)
            self.is_listening = False
            return response
        
        # Exit program
        elif "exit" in query or "stop" in query or "quit" in query:
            response = random.choice(farewell_responses)
            self.is_active = False
            return response
        
        # For other queries, use our simplified AI response system
        else:
            return self.search_free_answer(query)
    
    def run(self):
        """Main loop for the assistant"""
        while self.is_active:
            if not self.is_listening:
                self.wait_for_wake_word()
                continue
            
            query = self.listen()
            
            if query:
                response = self.execute_command(query)
                self.speak(response)
                
                # Check if we should keep listening or wait for wake word again
                if not self.is_listening:
                    continue
                    
                # Small pause before listening again
                time.sleep(1)

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run() 