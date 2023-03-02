import sys
import os
import json
import speech_recognition as sr 
import pyttsx3
from rich import print

COMMANDS = ["add", "remove", "edit", "complete", "list", "help", "logout", "exit"]
API_FILE = "API.json"

# might want to use threading
class Query:
    prompt: str
    command: str
    engine: pyttsx3.Engine
    openai_key: str

    def __init__(self, load: bool):
        if load:
            self.engine = pyttsx3.init()
            self.openai_key = self.get_apikey("OPENAI")

    def get_apikey(self, api: str, api_file: str = API_FILE):
        with open(api_file, "r") as f:
            return json.load(f)[api]

    def get_command(self, question: str, choices: list[str], default: str):
        c = ",".join(choices)
        print(question + f":[bold blue]{c}[/bold blue] [bold magenta]({default})[/bold magenta]")
        print("[bold yellow]Wait until ready...[/bold yellow]")
        self.engine.say(question)
        self.engine.runAndWait()
        raw_command = self.listen()
        user_command = True if question == "User to load/create" else False
        self.command = self.parse_command(raw_command, user_command=user_command)
        print("\n" + self.command)

    def parse_command(self, raw_command: str, user_command: bool = False):
        if user_command:
            return raw_command
        for word in raw_command.split():
            if word in COMMANDS:
                return word
        print("[red]Command not recognized[/red]")
        return self.get_command("Try again", [], "exit")


    def listen(self):
        try: 
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source,duration=0.5)
                print("[bold green]Ready[/bold green]")
                audio = r.listen(source)
            sys.stdout = open(os.devnull, 'w')
            raw_command = r.recognize_google(audio_data=audio,)
            sys.stdout = sys.__stdout__
            return raw_command.lower()
        except sr.UnknownValueError:
            print("[bold red]Unknown Value Error[/bold red]")
            sys.exit(1)
        except sr.RequestError:
            print("[bold red]Request Error[/bold red]")
            sys.exit(1)

    def generate_prompt(self):
        pass

    def generate_response(self):
        pass

    def read_response(self):
        pass

