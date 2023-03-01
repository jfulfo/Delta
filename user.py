import os
import subprocess
import sys
import json
from schedule import Schedule, EventEncoder, EventDecoder

USER_DIR = 'Users'

class User:
    """
    Used to relate a user to a schedule
    """
    name: str 
    schedule: Schedule

    def __init__(self, name: str):
        self.name = name
        if not os.path.exists(f'{USER_DIR}/{self.name}.json'):
            self.schedule = Schedule()
            self.create_user_dir()
            self.create_user()
        else:
            self.load_user()

    def load_user(self):
        """
        Loads a user's json file
        """
        with open(f'{USER_DIR}/{self.name}.json', 'r') as f:
            s = json.load(f, cls=EventDecoder)
            self.schedule = Schedule(events={s.name: s})

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
        with open(f'{USER_DIR}/{self.name}.json', 'w') as f:
            json.dump(self.schedule.events, f, cls=EventEncoder)

    def save(self):
        """
        Alias for create_user
        """
        self.create_user()

    def set_default_user(self):
        """
        Sets the default user
        """
        with open('default_user.txt', 'w') as f:
            f.write(self.name)

    def get_default_user(self):
        """
        Gets the default user
        """
        with open('default_user.txt', 'r') as f:
            return f.read()

    
