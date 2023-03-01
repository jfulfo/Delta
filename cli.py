import sys
import typer
from rich import print
from rich.prompt import Prompt
from schedule import Event
from datetime import date, time
from user import User
from query import Query

COMMANDS = ["add", "remove", "edit", "complete", "list", "help", "logout", "exit"]
ALLOWED_PARAMS = {"name": "string", "date": "YYYY-MM-DD", "start": "HH:MM", "end": "HH:MM", "priority": "int", "repeat": "int", "completed": "bool"}

class Shell:
    user: User
    speech: bool
    query: Query

    def __init__(self, user: User, speech: bool):
        self.user = user
        self.speech = speech
        if self.speech:
            self.query = Query(True)
        else:
            self.query = Query(False)

    def get_input(self, question: str, choices: list = [], default: str = "") -> str:
        if self.speech:
            return str(self.query.get_command(question, choices, default))
        else:
            if choices == [] or default == "":
                return Prompt.ask(question)
            return str(Prompt.ask(question, choices=choices, default=default))

    def run(self, command: str):
        match command.lower():
            case "add":
                name = self.get_input("Event name")

                s = self.get_input("Start and end time (HH:MM-HH:MM)")
                while True:
                    try:
                        start, end = s.split("-")
                        start = time.fromisoformat(start)
                        end = time.fromisoformat(end)
                        break
                    except ValueError:
                        print("[red]Invalid time format[/red]")
                        s = self.get_input("Start and end time (HH:MM-HH:MM)")
                while start > end:
                    print("[red]Start time must be before end time[/red]")
                    s = self.get_input("Start and end time (HH:MM-HH:MM)")
                    start, end = s.split("-")                
                    while True:
                        try:
                            start = time.fromisoformat(start)
                            end = time.fromisoformat(end)
                            break
                        except ValueError:
                            print("[red]Invalid time format[/red]")
                            s = self.get_input("Start and end time (HH:MM-HH:MM)")
                            start, end = s.split("-")

                dt = self.get_input("Date (YYYY-MM-DD)")
                while True:
                    try:
                        dt = date.fromisoformat(dt)
                        break
                    except ValueError:
                        print("[red]Invalid date format[/red]")
                        dt = self.get_input("Date (YYYY-MM-DD)")


                priority = self.get_input("Priority (0-3)", choices=["0", "1", "2", "3"], default="0")
                while priority not in ["0", "1", "2", "3"]:
                    print("[red]Priority must be an integer between 0 and 3[/red]")
                    priority = self.get_input("Priority (0-3)", choices=["0", "1", "2", "3"], default="0")
                priority = int(priority)

                repeat = self.get_input("Repeat every (val) days", default="0")
                while True:
                    try:
                        repeat = int(repeat)
                        break
                    except ValueError:
                        print("[red]Repeat must be an integer[/red]")
                        repeat = self.get_input("Repeat every (val) days")

                event = Event(name, (dt, start, end), priority, repeat, completed=False)
                print(event)
                self.user.schedule.add_event(event)
                self.user.save()

            case "remove":
                name = self.get_input("Event name")
                while name not in self.user.schedule.events:
                    print("[red]Event not found[/red]")
                    print(self.user.schedule)
                    name = self.get_input("Event name")
                self.user.schedule.remove_event(name)
                self.user.save()

            case "complete":
                name = self.get_input("Event name")
                while name not in self.user.schedule.events:
                    print("[red]Event not found[/red]")
                    print(self.user.schedule)
                    name = self.get_input("Event name")
                self.user.schedule.complete_event(name)
                self.user.save()

            case "edit":
                name = self.get_input("Event name")
                while name not in self.user.schedule.events:
                    print("[red]Event not found[/red]")
                    print(self.user.schedule)
                    name = self.get_input("Event name")
                event = self.user.schedule.events[name]

                param = self.get_input("Parameter to edit").lower()
                while param not in ALLOWED_PARAMS:
                    print("[red]Invalid parameter[/red]")
                    param = self.get_input("Parameter to edit").lower()

                val = self.get_input(f"New value ({ALLOWED_PARAMS[param]})")
                while True:
                    try:
                        if param == "name":
                            event.name = val
                        elif param == "date":
                            event.dt = date.fromisoformat(val)
                        elif param == "start":
                            event.start = time.fromisoformat(val)
                            while event.start > event.end:
                                print("[red]Start time must be before end time[/red]")
                                val = self.get_input(f"New value ({ALLOWED_PARAMS[param]})") 
                                event.start = time.fromisoformat(val)
                        elif param == "end":
                            event.end = time.fromisoformat(val)
                            while event.start > event.end:
                                print("[red]Start time must be before end time[/red]")
                                val = self.get_input(f"New value ({ALLOWED_PARAMS[param]})")
                                event.end = time.fromisoformat(val)
                        elif param == "priority":
                            event.priority = int(val)
                        elif param == "repeat":
                            event.repeat = int(val)
                        break
                    except ValueError:
                        print("[red]Invalid value[/red]")
                        val = self.get_input(f"New value ({ALLOWED_PARAMS[param]})")

                self.user.schedule.edit_event(event, param, val)
                print(event)
                self.user.save()

            case "list":
                if self.user.schedule.events == {}:
                    print("[red]No events[/red]")
                else:
                    print(self.user.schedule)

            case "help":
                print("[green]Commands[/green]:", ", ".join(COMMANDS))
            case "logout":
                pass

            case "exit":
                print("Exiting...")

            case _:
                print("[red]Invalid command[/red]")


def main(username: str, speech: bool, delete: bool = False):
    if username == "":
        with open('default_user.txt', 'r') as f:
            username = f.read()
    user = User(username)
    if delete:
        user.delete()
        print(f"User {username} deleted")
        sys.exit(0)
    print("[green]Commands[/green]:", ", ".join(COMMANDS))
    shell = Shell(user, speech)
    command = shell.get_input(f"{username}")
    while command != "exit":
        shell.run(command)
        command = shell.get_input(f"{username}")
        if command == "logout":
            username = shell.get_input("Username")
            user = User(username)
            command = shell.get_input(f"{username}")
    
if __name__ == "__main__":
    typer.run(main)
