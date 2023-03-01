import typer
from schedule import Schedule, Event, EventEncoder, EventDecoder
from datetime import date, time
from user import User

def main(command: str, username: str = ""):
    if username == "":
        with open('default_user.txt', 'r') as f:
            username = f.read()
    user = User(username)
    match command:
        case "add":
            name = typer.prompt("Event name")
            s = typer.prompt("Start and end time (HH:MM-HH:MM)")
            start, end = s.split("-")
            start = time.fromisoformat(start)
            end = time.fromisoformat(end)
            dt = typer.prompt("Date (YYYY-MM-DD)")
            dt = date.fromisoformat(dt)
            priority = typer.prompt("Priority (0-3)")
            repeat = typer.prompt("Repeat every (val) days")
            event = Event(name, (dt,start,end), priority, repeat)
            typer.echo(f"Added event \"{event}\"")
            user.schedule.add_event(event)
            user.save()

if __name__ == "__main__":
    typer.run(main)
