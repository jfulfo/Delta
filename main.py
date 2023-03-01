import os
import sys
import typer
from rich import print
from rich.prompt import Prompt
from query import Query

def main():
    cli = Prompt.ask("Do you want to run the CLI or GUI?", choices=["cli", "gui"], default="cli")
    speech = Prompt.ask("Do you want to use speech recognition and text-to-speech?", choices=["y", "n"], default="n")
    speech = True if speech == "y" else False
    if cli == "cli":
        if speech:
            q = Query(True)
            q.get_command("User to load/create", [], "")
            user = q.command
        else:
            user = Prompt.ask("User to load/create")
        os.system(f"python3 cli.py {user} {speech}")
    else:
        print("GUI is not yet implemented")
        sys.exit(1)

if __name__ == "__main__":
    main()
