import sys
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
        print(question + f"[bold blue]{c}[/bold blue] [bold magenta]{default}[/bold magenta]", end=" ")
        raw_command = self.listen()
        self.command = str(self.parse_command(raw_command))
        print(self.command)

    def parse_command(self, raw_command: str):
        for word in raw_command.split():
            if word in COMMANDS:
                return word
        print("[red]Command not recognized[/red]")
        return self.get_command("Try again", [], "exit")


    def listen(self):
        try: 
            r = sr.Recognizer()
            mic = sr.Microphone()
            self.engine.say("Taking input")
            self.engine.runAndWait()
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            raw_command = str(r.recognize_google(audio))
            return raw_command.lower()
        except sr.UnknownValueError:
            sys.exit(1)
        except sr.RequestError:
            sys.exit(1)

    def generate_prompt(self):
        pass

    def generate_response(self):
        pass

    def read_response(self):
        pass

