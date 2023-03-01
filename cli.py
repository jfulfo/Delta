import sys
import typer
from rich import print
from rich.prompt import Prompt
from schedule import Schedule, Event, EventEncoder, EventDecoder
from datetime import date, time
from user import User

COMMANDS = ["add", "remove", "edit", "complete", "list", "help", "logout", "exit"]
ALLOWED_PARAMS = {"name": "string", "date": "YYYY-MM-DD", "start": "HH:MM", "end": "HH:MM", "priority": "int", "repeat": "int", "completed": "bool"}

def run(command: str, user: User):
    match command.lower():
        case "add":
            name = Prompt.ask("Event name")

            s = Prompt.ask("Start and end time [pink](HH:MM-HH:MM)[/pink]")
            while True:
                try:
                    start, end = s.split("-")
                    start = time.fromisoformat(start)
                    end = time.fromisoformat(end)
                    break
                except ValueError:
                    print("[red]Invalid time format[/red]")
                    s = Prompt.ask("Start and end time (HH:MM-HH:MM)")
            while start > end:
                print("[red]Start time must be before end time[/red]")
                s = Prompt.ask("Start and end time (HH:MM-HH:MM)")
                start, end = s.split("-")                
                while True:
                    try:
                        start = time.fromisoformat(start)
                        end = time.fromisoformat(end)
                        break
                    except ValueError:
                        print("[red]Invalid time format[/red]")
                        s = Prompt.ask("Start and end time (HH:MM-HH:MM)")
                        start, end = s.split("-")

            dt = Prompt.ask("Date (YYYY-MM-DD)")
            while True:
                try:
                    dt = date.fromisoformat(dt)
                    break
                except ValueError:
                    print("[red]Invalid date format[/red]")
                    dt = Prompt.ask("Date (YYYY-MM-DD)")


            priority = Prompt.ask("Priority (0-3)", choices=["0", "1", "2", "3"], default="0")
            while priority not in ["0", "1", "2", "3"]:
                print("[red]Priority must be an integer between 0 and 3[/red]")
                priority = Prompt.ask("Priority (0-3)", choices=["0", "1", "2", "3"], default="0")
            priority = int(priority)

            repeat = Prompt.ask("Repeat every (val) days", default="0")
            while True:
                try:
                    repeat = int(repeat)
                    break
                except ValueError:
                    print("[red]Repeat must be an integer[/red]")
                    repeat = Prompt.ask("Repeat every (val) days")

            event = Event(name, (dt, start, end), priority, repeat, completed=False)
            print(event)
            user.schedule.add_event(event)
            user.save()

        case "remove":
            name = Prompt.ask("Event name")
            while name not in user.schedule.events:
                print("[red]Event not found[/red]")
                print(user.schedule)
                name = Prompt.ask("Event name")
            user.schedule.remove_event(name)
            user.save()

        case "complete":
            name = Prompt.ask("Event name")
            while name not in user.schedule.events:
                print("[red]Event not found[/red]")
                print(user.schedule)
                name = Prompt.ask("Event name")
            user.schedule.complete_event(name)
            user.save()

        case "edit":
            name = Prompt.ask("Event name")
            while name not in user.schedule.events:
                print("[red]Event not found[/red]")
                print(user.schedule)
                name = Prompt.ask("Event name")
            event = user.schedule.events[name]

            param = Prompt.ask("Parameter to edit").lower()
            while param not in ALLOWED_PARAMS:
                print("[red]Invalid parameter[/red]")
                param = Prompt.ask("Parameter to edit").lower()

            val = Prompt.ask(f"New value ({ALLOWED_PARAMS[param]})")
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
                            val = Prompt.ask(f"New value ({ALLOWED_PARAMS[param]})") 
                            event.start = time.fromisoformat(val)
                    elif param == "end":
                        event.end = time.fromisoformat(val)
                        while event.start > event.end:
                            print("[red]Start time must be before end time[/red]")
                            val = Prompt.ask(f"New value ({ALLOWED_PARAMS[param]})")
                            event.end = time.fromisoformat(val)
                    elif param == "priority":
                        event.priority = int(val)
                    elif param == "repeat":
                        event.repeat = int(val)
                    break
                except ValueError:
                    print("[red]Invalid value[/red]")
                    val = Prompt.ask(f"New value ({ALLOWED_PARAMS[param]})")

            user.schedule.edit_event(event, param, val)
            print(event)
            user.save()

        case "list":
            print(user.schedule)

        case "help":
            print("[green]Commands[/green]:", ", ".join(COMMANDS))
        case "logout":
            pass

        case "exit":
            print("Exiting...")

        case _:
            print("[red]Invalid command[/red]")


def main(username: str, delete: bool = False):
    if username == "":
        with open('default_user.txt', 'r') as f:
            username = f.read()
    user = User(username)
    if delete:
        user.delete()
        print(f"User {username} deleted")
        sys.exit(0)
    print("[green]Commands[/green]:", ", ".join(COMMANDS))
    command = Prompt.ask(f"{username}")
    while command != "exit":
        run(command, user)
        command = Prompt.ask(f"{username}").lower()
        if command == "logout":
            username = Prompt.ask("Username")
            user = User(username)
            command = Prompt.ask(f"{username}").lower()
    
if __name__ == "__main__":
    typer.run(main)
