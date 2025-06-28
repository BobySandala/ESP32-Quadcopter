import dearpygui.dearpygui as dpg

class StatusWindow:
    def __init__(self, tag="status_window", pos=(100, 100), size=(350, 120), ending=""):
        """Initializeaza clasa si valorile variabilelor"""
        self.tag = tag
        self.rollRegVals = ""
        self.pitchRegVals = ""
        self.yawRegVals = ""
        self.altitudeRegVals = ""

        # creaza o fereastra cu atributele primite
        with dpg.window(label=self.tag, pos=pos, 
                        width=size[0], height=size[1], tag=self.tag):
            # afisajul sirurilor de caractere este grupat, acestea sunt aliniate vertical
            with dpg.group(horizontal=False):
                # valoarea implicita si tagul pentru fiecare
                dpg.add_text("Se asteapta valori", tag="ROLL"+ending)
                dpg.add_text("Se asteapta valori", tag="PITCH"+ending)
                dpg.add_text("Se asteapta valori", tag="YAW"+ending)
                dpg.add_text("Se asteapta valori", tag="ALTITUDE"+ending)

    def update(self, reg, kp, ki, kd):
        """actualizeaza sirurile de caractere cu datele curente"""
        # in functie de tag si de valori, se creaza un sir de caractere pentru afisaj
        dpg.set_value(reg, reg + " | KP: " + kp + " | KI: " + ki + " | KD: " + kd)