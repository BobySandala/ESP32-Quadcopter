import dearpygui.dearpygui as dpg

class PIDWindow:
    def __init__(self, tag="status_window", pos=(100, 100), size=(350, 120)):
        self.tag = tag

        self.rollRegVals = ""
        self.pitchRegVals = ""
        self.yawRegVals = ""
        self.altitudeRegVals = ""

        with dpg.window(label="Status Window", pos=pos, width=size[0], height=size[1], tag=self.tag):
            with dpg.group(horizontal=False):
                dpg.add_text("Initializing...", tag="ROLL")
                dpg.add_text("Initializing...", tag="PITCH")
                dpg.add_text("Initializing...", tag="YAW")
                dpg.add_text("Initializing...", tag="ALTITUDE")

    def update(self, reg, kp, ki, kd):
        dpg.set_value(reg, reg + " | KP: " + f"{kp: .3f}" + " | KI: " + f"{ki: .3f}" + " | KD: " + f"{kd: .3f}")
