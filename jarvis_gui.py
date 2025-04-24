import os
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import pyttsx3
from PIL import Image, ImageTk
import speech_recognition as sr
from jarvis import JarvisAssistant

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S Personal Assistant")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg='#1E1E1E')
        
        # Set icon if available
        try:
            self.root.iconbitmap('jarvis_icon.ico')
        except:
            pass
        
        # Initialize JARVIS assistant
        self.jarvis = JarvisAssistant()
        self.jarvis.speak = self.speak  # Override speak method
        
        # Status variables
        self.is_listening = False
        self.is_speaking = False
        self.status_text = tk.StringVar()
        self.status_text.set("Initializing...")
        
        # Initialize speech engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180)
        
        # Create GUI elements
        self.create_widgets()
        
        # Start the assistant
        self.status_text.set("Say 'Jarvis' to begin")
        threading.Thread(target=self.listen_for_wake_word, daemon=True).start()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1E1E1E')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="J.A.R.V.I.S",
            font=("Helvetica", 24, "bold"),
            fg="#00BFFF",
            bg="#1E1E1E"
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Just A Rather Very Intelligent System",
            font=("Helvetica", 12),
            fg="#CCCCCC",
            bg="#1E1E1E"
        )
        subtitle_label.pack(pady=5)
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2D2D2D', relief=tk.GROOVE, bd=2)
        status_frame.pack(fill=tk.X, pady=20)
        
        # Status label
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_text,
            font=("Helvetica", 10),
            fg="#00BFFF",
            bg="#2D2D2D",
            padx=10,
            pady=10
        )
        status_label.pack(fill=tk.X)
        
        # Progress bar (for visual feedback)
        self.progress = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='indeterminate'
        )
        self.progress.pack(pady=10)
        
        # Conversation history
        history_frame = tk.Frame(main_frame, bg='#2D2D2D', relief=tk.GROOVE, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        history_label = tk.Label(
            history_frame,
            text="Conversation History",
            font=("Helvetica", 10, "bold"),
            fg="#FFFFFF",
            bg="#2D2D2D",
            padx=10,
            pady=5
        )
        history_label.pack(anchor=tk.W)
        
        self.conversation = scrolledtext.ScrolledText(
            history_frame,
            font=("Courier", 10),
            fg="#FFFFFF",
            bg="#3D3D3D",
            wrap=tk.WORD,
            width=70,
            height=15
        )
        self.conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.conversation.config(state=tk.DISABLED)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#1E1E1E')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.listen_button = tk.Button(
            button_frame,
            text="Listen",
            font=("Helvetica", 10),
            command=self.toggle_listening,
            bg="#007ACC",
            fg="white",
            width=15,
            height=2
        )
        self.listen_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            font=("Helvetica", 10),
            command=self.stop_jarvis,
            bg="#FF4500",
            fg="white",
            width=15,
            height=2
        )
        self.stop_button.pack(side=tk.RIGHT, padx=5)

    def update_conversation(self, speaker, text):
        self.conversation.config(state=tk.NORMAL)
        self.conversation.insert(tk.END, f"{speaker}: {text}\n\n")
        self.conversation.see(tk.END)
        self.conversation.config(state=tk.DISABLED)

    def speak(self, text):
        self.is_speaking = True
        self.status_text.set("Speaking...")
        self.update_conversation("JARVIS", text)
        
        # Use threading to avoid freezing the GUI
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
            self.status_text.set("Listening..." if self.is_listening else "Say 'Jarvis' to begin")
            
        threading.Thread(target=speak_thread, daemon=True).start()

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.status_text.set("Listening...")
            self.progress.start(10)
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                self.status_text.set("Processing...")
                
                try:
                    text = recognizer.recognize_google(audio).lower()
                    self.update_conversation("You", text)
                    return text
                except sr.UnknownValueError:
                    self.status_text.set("Sorry, I didn't catch that")
                    time.sleep(2)
                except sr.RequestError:
                    self.status_text.set("Sorry, my speech service is down")
                    time.sleep(2)
            except sr.WaitTimeoutError:
                self.status_text.set("Timeout: No speech detected")
                time.sleep(2)
            finally:
                self.progress.stop()
                
        return ""

    def listen_for_wake_word(self):
        recognizer = sr.Recognizer()
        while True:
            if self.is_listening:
                time.sleep(0.1)
                continue
                
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, phrase_time_limit=3)
                    
                    try:
                        text = recognizer.recognize_google(audio).lower()
                        if "jarvis" in text:
                            self.is_listening = True
                            self.status_text.set("I'm listening...")
                            self.progress.start(10)
                            
                            response = self.jarvis.execute_command("hello")
                            self.speak(response)
                            
                            # Start the conversation loop
                            threading.Thread(target=self.conversation_loop, daemon=True).start()
                    except:
                        pass
            except:
                time.sleep(0.1)

    def conversation_loop(self):
        while self.is_listening:
            # Wait if currently speaking
            while self.is_speaking:
                time.sleep(0.1)
                
            # Get user input
            user_input = self.listen()
            
            if user_input:
                # Process the command
                response = self.jarvis.execute_command(user_input)
                
                # Check if we should stop listening
                if "goodbye" in user_input or "bye" in user_input:
                    self.is_listening = False
                    self.progress.stop()
                    self.status_text.set("Say 'Jarvis' to begin")
                
                # Speak the response
                self.speak(response)
            
            time.sleep(0.1)

    def toggle_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.listen_button.config(text="Listen")
            self.status_text.set("Say 'Jarvis' to begin")
            self.progress.stop()
        else:
            self.is_listening = True
            self.listen_button.config(text="Listening...")
            self.status_text.set("I'm listening...")
            self.progress.start(10)
            
            # Greet the user
            response = self.jarvis.execute_command("hello")
            self.speak(response)
            
            # Start the conversation loop
            threading.Thread(target=self.conversation_loop, daemon=True).start()

    def stop_jarvis(self):
        self.is_listening = False
        self.status_text.set("Stopping...")
        self.progress.stop()
        self.root.after(1000, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop() 