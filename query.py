import sys
import os
import json
import pyttsx3
import sounddevice as sd 
from scipy.io.wavfile import write
import openai
from rich import print

COMMANDS = ["add", "remove", "edit", "complete", "list", "help", "logout", "exit"]
API_FILE = "API.json"
RATE = 44100 
DURATION = 3
AUDIO_FILE = "audio.wav"

# might want to use threading
class Query:
    prompt: str
    command: str
    engine: pyttsx3.Engine

    def __init__(self, load: bool):
        if load:
            self.engine = pyttsx3.init()
            openai.api_key = self.get_apikey("OPENAI")

    def get_apikey(self, api: str, api_file: str = API_FILE):
        with open(api_file, "r") as f:
            return json.load(f)[api]

    def get_command(self, question: str, choices: list[str], default: str):
        c = ",".join(choices)
        print(question + f":[bold blue]{c}[/bold blue] [bold magenta]({default})[/bold magenta]")
        print("[bold yellow]Wait until ready...[/bold yellow]")
        self.engine.say(question)
        self.engine.runAndWait()
        print("[bold green]Recording[/bold green]")
        record = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=2)
        sd.wait()
        write(AUDIO_FILE, RATE, record)
        print("[bold yellow]Processing...[/bold yellow]")
        audio_file = open(AUDIO_FILE, "rb")
        raw_command = openai.Audio.transcribe("whisper-1", audio_file)
        print("[bold green]Done[/bold green]")
        raw_command = str(raw_command["text"]).lower()
        user_command = True if question == "User to load/create" else False
        if user_command:
            self.command = raw_command.replace(".", "") 
        else:
            for word in raw_command.split():
                if word in choices:
                    self.command = word 
                    break
                elif len(choices) == 0:
                    self.command = word
                    break
        print("\n" + self.command)

    def generate_prompt(self):
        pass

    def generate_response(self):
        pass

