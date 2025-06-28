import dearpygui.dearpygui as dpg

class PID_Vals:
    def __init__(self, pos=(0, 0), tag="", window_size=(0, 0), testbox_size=(0,0)):
        """Initializeaza clasa si valorile variabilelor"""
        self.pos, self.tag = pos, tag
        self.size = (100, 50) if window_size == (0, 0) else window_size
        self.textbox_size = (80, 30) if testbox_size == (0, 0) else testbox_size
        self.tag = f"input_{id(self)}" if tag == "" else tag
        self.kp = self.ki = self.kd = "0"
        self.is_input_error_kp = self.is_input_error_ki = self.is_input_error_kd = False
        self.a = 0
        # functia call back pentru trimiterea datelor
        self.has_external_callback = False
        
        # creaza o fereastra cu atributele date
        with dpg.window(label="PID Input Window", pos=self.pos, 
                        width=self.size[0], height=self.size[1], 
                        tag=self.tag, autosize=False):
            # grupeaza campurile de input, ordonate orizontal
            with dpg.group(horizontal=True):
                # creaza 3 campuri de input si le atribuie cate o functie callback
                self.input_txt_kp = dpg.add_input_text(
                    default_value="0",
                    width=testbox_size[0],
                    height=testbox_size[1],
                    callback=self.set_kp,
                    tag=f"{self.tag}_KP",
                    label="KP")
                self.input_txt_ki = dpg.add_input_text(
                    default_value="0",
                    width=testbox_size[0],
                    height=testbox_size[1],
                    callback=self.set_ki,
                    tag=f"{self.tag}_KI",
                    label="KI")
                self.input_txt_kd = dpg.add_input_text(
                    default_value="0",
                    width=testbox_size[0],
                    height=testbox_size[1],
                    callback=self.set_kd,
                    tag=f"{self.tag}_KD",
                    label="KD")
            
            # grupeaza butoanele cu rol de submit catre arduino
            with dpg.group(horizontal=True):
                btn_roll = dpg.add_button(label="ROLL", callback=self.send_values)
                btn_pitch = dpg.add_button(label="PITCH", callback=self.send_values)
                btn_yaw = dpg.add_button(label="YAW", callback=self.send_values)
                btn_alt = dpg.add_button(label="ALTITUDE", callback=self.send_values)
            with dpg.group(horizontal=True):
                btn_roll = dpg.add_button(label="ROLL_E", callback=self.send_values)
                btn_pitch = dpg.add_button(label="PITCH_E", callback=self.send_values)
                btn_yaw = dpg.add_button(label="YAW_E", callback=self.send_values)
                btn_alt = dpg.add_button(label="ALTITUDE_E", callback=self.send_values)
            with dpg.group(horizontal=True):
                self.input_txt_kd = dpg.add_input_text(
                    default_value="0",
                    width=testbox_size[0],
                    height=testbox_size[1],
                    callback=self.set_a,
                    tag=f"{self.tag}_A",
                    label="PT1_A")
                btn_pt1_a = dpg.add_button(label="PT1_A", callback=self.send_a_pt1)
            # creaza un camp destinat afisarii de erori
            dpg.add_text("", tag="error_field")

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def set_error_field(self):
        if self.is_input_error_kd or self.is_input_error_ki or self.is_input_error_kd:
            dpg.set_value("error_field", "Eroare la introducerea datelor")
        else:
            dpg.set_value("error_field", "")

    def send_a_pt1(self, sender):
        """functia callback a butoanelor pentru submit"""
        # verifica daca are functie callback
        if self.has_external_callback == False:
            self.set_error_field("Functia Callback neinitializata")
            return
        # verifica daca datele introduse sunt valide
        if self.is_input_error_kd or self.is_input_error_ki or self.is_input_error_kd:
            self.set_error_field("Valori invalide in campurile de input")
            return
        
        # apeleaza functia callback cu parametrul label
        self.external_callback(dpg.get_item_label(sender))

    def set_a(self, sender):
        """salveaza valoarea introdusa in campul input asociat intr-o variabila interna"""
        # pastreaza valoarea ca sir de caractere
        self.a = dpg.get_value(sender)

        # in caz de valoare invalida se afiseaza un mesaj in campul de eroare
        if self.is_number(self.a):
            self.is_input_error_kp = False
            self.set_error_field()
        else:
            self.is_input_error_kp = True
            self.set_error_field()

    def set_kp(self, sender):
        """salveaza valoarea introdusa in campul input asociat intr-o variabila interna"""
        # pastreaza valoarea ca sir de caractere
        self.kp = dpg.get_value(sender)

        # in caz de valoare invalida se afiseaza un mesaj in campul de eroare
        if self.is_number(self.kp):
            self.is_input_error_kp = False
            self.set_error_field()
        else:
            self.is_input_error_kp = True
            self.set_error_field()

    def set_ki(self, sender):
        """salveaza valoarea introdusa in campul input asociat intr-o variabila interna"""
        self.ki = dpg.get_value(sender)

        # in caz de valoare invalida se afiseaza un mesaj in campul de eroare
        if self.is_number(self.ki):
            self.is_input_error_ki = False
            self.set_error_field()
        else:
            self.is_input_error_ki = True
            self.set_error_field()

    def set_kd(self, sender):
        """salveaza valoarea introdusa in campul input asociat intr-o variabila interna"""
        self.kd = dpg.get_value(sender)

        # in caz de valoare invalida se afiseaza un mesaj in campul de eroare
        if self.is_number(self.kd):
            self.is_input_error_kd = False
            self.set_error_field()
        else:
            self.is_input_error_kd = True
            self.set_error_field()

    def set_external_callback(self, callback):
        """seteaza functia de callback pentru trimiterea prin udp"""
        self.external_callback = callback
        self.has_external_callback = True
    
    def send_values(self, sender):
        """functia callback a butoanelor pentru submit"""
        # verifica daca are functie callback
        if self.has_external_callback == False:
            self.set_error_field("Functia Callback neinitializata")
            return
        # verifica daca datele introduse sunt valide
        if self.is_input_error_kd or self.is_input_error_ki or self.is_input_error_kd:
            self.set_error_field("Valori invalide in campurile de input")
            return
        
        # apeleaza functia callback cu parametrul label
        self.external_callback(dpg.get_item_label(sender))

class GraphLegend:
    def __init__(self, pos=(0, 0), size=(200, 100), tag="legend_window", 
                 real_color=(0, 255, 0, 255), desired_color=(255, 0, 0, 255)):
        """
        Creates a window with two colored text items acting as a legend.
        """
        self.tag = tag
        self.real_color = (0, 122, 204, 255)  
        self.desired_color = (210, 105, 30, 255) 


        with dpg.window(label="Legend", pos=pos, width=size[0], height=size[1], tag=self.tag, no_title_bar=True, no_resize=True):
            with dpg.group(horizontal=False):
                dpg.add_text("Legenda:", color=(150, 150, 150, 255))
                dpg.add_text("Graficul valorilor reale", color=self.real_color)
                dpg.add_text("Graficul valorilor dorite", color=self.desired_color)
