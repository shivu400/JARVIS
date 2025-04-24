#!/usr/bin/env python3
import sys
import os
import importlib.util
import argparse

def check_dependencies():
    """Check if all required dependencies are installed"""
    dependencies = [
        "speech_recognition",
        "pyttsx3",
        "requests",
        "wikipedia",
        "dotenv"
    ]
    
    gui_dependencies = [
        "PIL",
        "tkinter"
    ]
    
    missing = []
    for dep in dependencies:
        if importlib.util.find_spec(dep) is None:
            missing.append(dep)
    
    if missing:
        print("Missing required dependencies:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nPlease install them using: pip install -r requirements.txt")
        return False
    
    return True

def run_cli():
    """Run JARVIS in command line mode"""
    print("Starting JARVIS in CLI mode...")
    from jarvis import JarvisAssistant
    assistant = JarvisAssistant()
    assistant.run()

def run_gui():
    """Run JARVIS with GUI interface"""
    print("Starting JARVIS with GUI...")
    import tkinter as tk
    from jarvis_gui import JarvisGUI
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant")
    parser.add_argument("--cli", action="store_true", help="Run in command line mode")
    parser.add_argument("--gui", action="store_true", help="Run with GUI interface")
    args = parser.parse_args()
    
    # Check if dependencies are installed
    if not check_dependencies():
        return
    
    # Determine which mode to run
    if args.cli:
        run_cli()
    elif args.gui:
        run_gui()
    else:
        # If no mode specified, ask the user
        print("Welcome to JARVIS AI Assistant!")
        print("1. Run in command line mode")
        print("2. Run with GUI interface")
        choice = input("Enter your choice (1/2): ")
        
        if choice == "1":
            run_cli()
        elif choice == "2":
            run_gui()
        else:
            print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main() 