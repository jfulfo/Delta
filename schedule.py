import os
import subprocess
from datetime import date, time
from json import JSONEncoder, JSONDecoder

class Event:
    """
    A class to represent an event to be stored in a schedule.
    """
    name: str
    datetimes: tuple[date,time,time]
    priority: int = 0
    repeat: int = 0 # repeats every x days, 0 means no repeat

    def __init__(self, name: str, times: tuple[date,time,time], priority: int, repeat: int):
        
        self.name = name
        self.datetimes = times
        self.priority = priority
        self.repeat = repeat

    def __str__(self):
        return f"""{self.name}:
        {self.datetimes[0]} {self.datetimes[1]} - {self.datetimes[2]}
        Priority: {self.priority}
        Repeat: {self.repeat}"""

    def __dict__(self):
        return {
            "name": self.name,
            "date": f"{self.datetimes[0]}",
            "start": f"{self.datetimes[1]}",
            "end": f"{self.datetimes[2]}",
            "priority": self.priority,
            "repeat": self.repeat
        }

class EventEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__()

class EventDecoder(JSONDecoder):
    def decode(self, o):
        d = super().decode(o)
        d = d[list(d.keys())[0]]
        return Event(d["name"], (d["date"], d["start"], d["end"]), d["priority"], d["repeat"])

class Schedule:
    """
    Used to store data about a user's schedule
    """
    events: dict[str, Event]

    def __init__(self, **kwargs):
        self.events = kwargs.get("events", {})

    def add_event(self, event: Event):
        """
        Adds an event to the schedule
        """
        self.events[event.name] = event

