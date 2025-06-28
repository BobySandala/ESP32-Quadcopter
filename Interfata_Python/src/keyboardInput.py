import keyboard
import json

class KeyboardInput:
    def __init__(self):
        self.state = {
            'w': False,
            'a': False,
            's': False,
            'd': False,
            'space': False,
            'shift': False
        }
        self.prev_state = self.state.copy()

    def update_state(self):
        # Save previous state
        self.prev_state = self.state.copy()
        
        # Update current state
        self.state['w'] = keyboard.is_pressed('w')
        self.state['a'] = keyboard.is_pressed('a')
        self.state['s'] = keyboard.is_pressed('s')
        self.state['d'] = keyboard.is_pressed('d')
        self.state['space'] = keyboard.is_pressed('space')
        self.state['shift'] = keyboard.is_pressed('shift')

    def has_changed(self):
        return self.state != self.prev_state

    def get_state(self):
        # Add a 'kbd' key for compatibility with your original format
        return {
            'kbd': "kbd",
            **self.state
        }

    def to_json(self):
        # Convert the current state to a pretty JSON string
        return json.dumps(self.get_state(), indent=4)