import os
import subprocess
from datetime import date, time
from json import JSONEncoder, JSONDecoder
from rich import print

class Event:
    """
    A class to represent an event to be stored in a schedule.
    """
    name: str
    dt: date
    start: time 
    end: time
    priority: int = 0
    repeat: int = 0 # repeats every x days, 0 means no repeat
    completed: bool = False

    def __init__(self, name: str, times: tuple[date,time,time], priority: int, repeat: int, completed: bool):
        
        self.name = name
        self.dt = times[0]
        self.start = times[1]
        self.end = times[2]
        self.priority = priority
        self.repeat = repeat
        self.completed = completed

    def __str__(self):
        return f"""{self.name}:
        Date: {self.dt} 
        Time: {self.start} - {self.end}
        Priority: {self.priority}
        Repeat: {self.repeat}
        Completed: {self.completed}"""


    def __dict__(self):
        return {
            "name": self.name,
            "date": f"{self.dt}",
            "start": f"{self.start}",
            "end": f"{self.end}",
            "priority": self.priority,
            "repeat": self.repeat,
            "completed": self.completed
        }

    def edit(self, param: str, value: str):
        """
        Edits an event's parameters.
        """
        match param:
            case "name":
                self.name = value
            case "date":
                self.dt = date.fromisoformat(value)
            case "start":
                self.start = time.fromisoformat(value)
            case "end":
                self.end = time.fromisoformat(value)
            case "priority":
                self.priority = int(value)
            case "repeat":
                self.repeat = int(value)
            case "completed":
                self.completed = bool(value)

class EventEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__()

class EventDecoder(JSONDecoder):
    def decode(self, o):
        d = super().decode(o)
        d = d[list(d.keys())[0]]
        return Event(d["name"], (d["date"], d["start"], d["end"]), d["priority"], d["repeat"], d["completed"])

class Schedule:
    """
    Used to store data about a user's schedule
    """
    events: dict[str, Event]

    def __init__(self, **kwargs):
        self.events = kwargs.get("events", {})

    def __str__(self):
        s = "\n"
        for event in self.events.values():
            s += f"{event}\n"
        return s

    def add_event(self, event: Event):
        """
        Adds an event to the schedule
        """
        self.events[event.name] = event

    def remove_event(self, event: str):
        """
        Removes an event from the schedule
        """
        del self.events[event]

    def complete_event(self, event: str):
        """
        Marks an event as completed
        """
        self.events[event].completed = True

    def edit_event(self, event: Event, param: str, value: str):
        """
        Edits an event's parameters.
        """
        if param == "name":
            self.events[value] = self.events.pop(list(self.events.keys())[0])
        self.events[event.name].edit(param, value)

    def get_event(self, event: str):
        """
        Gets an event from the schedule
        """
        try:
            return self.events[event]
        except KeyError:
            raise KeyError("Event not found.")

class ScheduleEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class ScheduleDecoder(JSONDecoder):
    def decode(self, o):
        d = super().decode(o)
        for event in d:
            d[event] = Event(d[event]["name"], (d[event]["date"], d[event]["start"], d[event]["end"]), d[event]["priority"], d[event]["repeat"], d[event]["completed"])
        return dict(d)

