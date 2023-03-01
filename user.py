import os
import subprocess
import sys
import json
from schedule import Schedule, EventEncoder, EventDecoder, ScheduleEncoder, ScheduleDecoder
from rich.prompt import Confirm

USER_DIR = "Users"

class User:
    """
    Used to relate a user to a schedule
    """
    name: str 
    schedule: Schedule

    def __init__(self, name: str):
        self.name = name
        if not os.path.exists(f"{USER_DIR}/{self.name}.json"):
            answer = Confirm.ask(f"User {self.name} does not exist. Would you like to create it?", default=True)
            if answer:
                self.schedule = Schedule()
                self.create_user_dir()
                self.create_user()
            else:
                sys.exit(0)
        else:
            try:
                self.load_user()
            except:
                answer = Confirm.ask(f"User {self.name} is corrupted. Would you like to delete it?", default=True)
                if answer:
                    self.schedule = Schedule()
                    self.create_user_dir()
                    self.create_user()
                else:
                    sys.exit(0)

    def load_user(self):
        """
        Loads a user's json file
        """
        with open(f"{USER_DIR}/{self.name}.json", "r") as f:
            self.schedule = Schedule(events=json.load(f, cls=ScheduleDecoder))

    def create_user_dir(self):
        """
        Creates a directory for the users
        """
        if not os.path.exists(USER_DIR):
            os.mkdir(USER_DIR)

    def create_user(self):
        """
        Creates a user's json file
        """
        with open(f"{USER_DIR}/{self.name}.json", "w") as f:
            json.dump(self.schedule.events, f, cls=EventEncoder,indent=4)

    def save(self):
        """
        Alias for create_user
        """
        self.create_user()

    def delete(self):
        """
        Deletes the user's json file
        """
        os.remove(f"{USER_DIR}/{self.name}.json")

    def set_default_user(self):
        """
        Sets the default user to the current user
        """
        with open("default_user.txt", "w") as f:
            f.write(self.name)

    def get_default_user(self):
        """
        Gets the default user
        """
        with open("default_user.txt", "r") as f:
            return f.read()

    
