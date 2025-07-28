"""
Command Pattern - Encapsulates requests as objects
Common interview question: Undo/Redo functionality, Remote control
"""

from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass


class Light:
    def __init__(self, location: str):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} light is ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} light is OFF")


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()


class RemoteControl:
    def __init__(self):
        self.commands: List[Command] = []
        self.last_command: Command = None
    
    def set_command(self, slot: int, command: Command):
        if len(self.commands) <= slot:
            self.commands.extend([None] * (slot + 1 - len(self.commands)))
        self.commands[slot] = command
    
    def press_button(self, slot: int):
        if slot < len(self.commands) and self.commands[slot]:
            self.commands[slot].execute()
            self.last_command = self.commands[slot]
    
    def press_undo(self):
        if self.last_command:
            self.last_command.undo()


# Usage example
if __name__ == "__main__":
    living_room_light = Light("Living Room")
    bedroom_light = Light("Bedroom")
    
    living_room_on = LightOnCommand(living_room_light)
    living_room_off = LightOffCommand(living_room_light)
    bedroom_on = LightOnCommand(bedroom_light)
    
    remote = RemoteControl()
    remote.set_command(0, living_room_on)
    remote.set_command(1, living_room_off)
    remote.set_command(2, bedroom_on)
    
    remote.press_button(0)  # Turn on living room light
    remote.press_button(2)  # Turn on bedroom light
    remote.press_undo()     # Undo last command