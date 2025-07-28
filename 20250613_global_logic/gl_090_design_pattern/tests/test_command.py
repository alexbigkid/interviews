import unittest
from io import StringIO
import sys
from src.design_patterns.command import Light, LightOnCommand, LightOffCommand, RemoteControl


class TestCommand(unittest.TestCase):
    
    def setUp(self):
        self.light = Light("Living Room")
        self.on_command = LightOnCommand(self.light)
        self.off_command = LightOffCommand(self.light)
        self.remote = RemoteControl()
    
    def test_light_on_command(self):
        """Test light on command execution"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.on_command.execute()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertTrue(self.light.is_on)
        self.assertIn("Living Room light is ON", output)
    
    def test_light_off_command(self):
        """Test light off command execution"""
        self.light.turn_on()  # Start with light on
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.off_command.execute()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertFalse(self.light.is_on)
        self.assertIn("Living Room light is OFF", output)
    
    def test_command_undo(self):
        """Test command undo functionality"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Turn on light, then undo
        self.on_command.execute()
        self.assertTrue(self.light.is_on)
        
        self.on_command.undo()
        self.assertFalse(self.light.is_on)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Living Room light is ON", output)
        self.assertIn("Living Room light is OFF", output)
    
    def test_remote_control_set_command(self):
        """Test setting commands on remote control"""
        self.remote.set_command(0, self.on_command)
        self.remote.set_command(1, self.off_command)
        
        self.assertEqual(len(self.remote.commands), 2)
        self.assertIs(self.remote.commands[0], self.on_command)
        self.assertIs(self.remote.commands[1], self.off_command)
    
    def test_remote_control_press_button(self):
        """Test pressing buttons on remote control"""
        self.remote.set_command(0, self.on_command)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.remote.press_button(0)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertTrue(self.light.is_on)
        self.assertIn("Living Room light is ON", output)
        self.assertIs(self.remote.last_command, self.on_command)
    
    def test_remote_control_undo(self):
        """Test undo functionality on remote control"""
        self.remote.set_command(0, self.on_command)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.remote.press_button(0)  # Turn on light
        self.remote.press_undo()     # Undo (turn off light)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertFalse(self.light.is_on)
        self.assertIn("Living Room light is ON", output)
        self.assertIn("Living Room light is OFF", output)
    
    def test_remote_control_invalid_slot(self):
        """Test pressing invalid slot doesn't crash"""
        try:
            self.remote.press_button(99)  # Non-existent slot
        except Exception as e:
            self.fail(f"Pressing invalid slot raised {e}")
    
    def test_undo_without_previous_command(self):
        """Test undo without previous command doesn't crash"""
        try:
            self.remote.press_undo()
        except Exception as e:
            self.fail(f"Undo without previous command raised {e}")


if __name__ == '__main__':
    unittest.main()