import keyboard
import comunication_control
from UI_PID import PID_Vals, GraphLegend
import asyncio
import config
from graphClass import Graph
import dearpygui.dearpygui as dpg
import json
from PIDWindow import StatusWindow
from keyboardInput import KeyboardInput

#initializeaza viewport-ul si creeaza instantele celor 4 grafice
dpg.create_context()

legend = GraphLegend(pos=config.LEGEND_POSITION, size=config.LEGEND_SIZE)

# valorile din fisierul config sunt atribuite graficelor
graph1 = Graph(data_length=config.GRAPH_1_DATA_LEN, 
                pos=config.GRAPH_1_POS, 
                tag=config.GRAPH_1_TITLE, 
                size=config.GRAPH_1_SIZE)

graph2 = Graph(data_length=config.GRAPH_2_DATA_LEN, 
                pos=config.GRAPH_2_POS, 
                tag=config.GRAPH_2_TITLE, 
                size=config.GRAPH_2_SIZE)

graph3 = Graph(data_length=config.GRAPH_3_DATA_LEN, 
                pos=config.GRAPH_3_POS, 
                tag=config.GRAPH_3_TITLE, 
                size=config.GRAPH_3_SIZE)

graph4 = Graph(data_length=config.GRAPH_4_DATA_LEN, 
                pos=config.GRAPH_4_POS, 
                tag=config.GRAPH_4_TITLE, 
                size=config.GRAPH_4_SIZE)

graph5 = Graph(data_length=config.GRAPH_5_DATA_LEN, 
                pos=config.GRAPH_5_POS, 
                tag=config.GRAPH_5_TITLE, 
                size=config.GRAPH_5_SIZE)

graph6 = Graph(data_length=config.GRAPH_6_DATA_LEN, 
                pos=config.GRAPH_6_POS, 
                tag=config.GRAPH_6_TITLE, 
                size=config.GRAPH_6_SIZE)

graph7 = Graph(data_length=config.GRAPH_7_DATA_LEN, 
                pos=config.GRAPH_7_POS, 
                tag=config.GRAPH_7_TITLE, 
                size=config.GRAPH_7_SIZE)

graph8 = Graph(data_length=config.GRAPH_8_DATA_LEN, 
                pos=config.GRAPH_8_POS, 
                tag=config.GRAPH_8_TITLE, 
                size=config.GRAPH_8_SIZE)

# este creat obiectul ferestrei de submit, sunt atribuite valorile din config
pid_vals = PID_Vals(window_size=config.PID_VALS_WINDOW_SIZE,
                    pos=config.PID_VALS_WINDOW_POS,
                    testbox_size=config.PID_VALS_INPUT_SIZE)

# este creat obiectul ferestrei de vizualizare a datelor PID
statusWindow = StatusWindow(tag="PID_Intern",
                            pos=config.PID_STATUS_WINDOW_POS,
                            size=config.PID_STATUS_WINDOW_SIZE)
# este creat obiectul ferestrei de vizualizare a datelor PID
statusWindow2 = StatusWindow(tag="PID_Extern",
                            ending="_E",
                            pos=config.PID_STATUS_WINDOW_2_POS,
                            size=config.PID_STATUS_WINDOW_2_SIZE)

# este creat viewport-ul si afisat
dpg.create_viewport(title=config.WINDOW_TITLE, 
                    width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)
dpg.setup_dearpygui()
dpg.show_viewport()

# variabilele cu valori implicite
roll = pitch = yaw = altitude = dt = 0.0
altitude_dt = roll_dt = pitch_dt = yaw_dt = 0.0
sp_altitude = sp_roll = sp_pitch = sp_yaw = 0.0
sp_dt_altitude = sp_dt_roll = sp_dt_pitch = sp_dt_yaw = 0.0
reg = kp = ki = kd = ""

def handle_incoming_data(data, addr):
    """Se ocupa cu manevrarea diferita a celor doua 
    variante de fisier json care pot fi citite"""
    global dt, reg, kp, ki, kd
    global altitude, roll, pitch, yaw
    global altitude_dt, roll_dt, pitch_dt, yaw_dt
    global sp_altitude, sp_roll, sp_pitch, sp_yaw
    global sp_dt_altitude, sp_dt_roll, sp_dt_pitch, sp_dt_yaw
    try:
        parsed = json.loads(data)
        # in cazul in care json-ul primit are campul "reg" acesta contine 
        # valorile constantelor PID
        # actualizeaza variabilele globale pentru a fi folosite in bucla principala
        if "reg" in parsed:
            reg = parsed.get("reg", reg)
            kp = parsed.get("kp",kp)
            ki = parsed.get("ki", ki)
            kd = parsed.get("kd", kd)
            statusWindow2.update(reg=reg, kp=kp, ki=ki, kd=kd)
            statusWindow.update(reg=reg, kp=kp, ki=ki, kd=kd)
        # altfel acesta contine datele de zbor
        else:
            roll = parsed.get("roll", roll)
            pitch = parsed.get("pitch", pitch)
            yaw = parsed.get("yaw", pitch)
            altitude = parsed.get("altitude", altitude)

            altitude_dt = parsed.get("altitude_dt", altitude_dt)
            roll_dt = parsed.get("roll_dt", roll_dt)
            pitch_dt = parsed.get("pitch_dt", pitch_dt)
            yaw_dt = parsed.get("yaw_dt", yaw_dt)

            sp_altitude = parsed.get("sp_altitude", sp_altitude)
            sp_roll = parsed.get("sp_roll", sp_roll)
            sp_pitch = parsed.get("sp_pitch", sp_pitch)
            sp_yaw = parsed.get("sp_yaw", sp_yaw)

            sp_dt_altitude = parsed.get("sp_dt_altitude", sp_dt_altitude)
            sp_dt_roll = parsed.get("sp_dt_roll", sp_dt_roll)
            sp_dt_pitch = parsed.get("sp_dt_pitch", sp_dt_pitch)
            sp_dt_yaw = parsed.get("sp_dt_yaw", sp_dt_yaw)

            # actualizeaza fiecare grafic cu noile valori citite in mod asincron
            graph1.update_graph(new_value_1=altitude, new_value_2=sp_altitude)
            graph2.update_graph(new_value_1=roll, new_value_2=sp_roll)
            graph3.update_graph(new_value_1=pitch, new_value_2=sp_pitch)
            graph4.update_graph(new_value_1=yaw, new_value_2=sp_yaw)

            graph5.update_graph(new_value_1=altitude_dt, new_value_2=sp_dt_altitude)
            graph6.update_graph(new_value_1=roll_dt, new_value_2=sp_dt_roll)
            graph7.update_graph(new_value_1=pitch_dt, new_value_2=sp_dt_pitch)
            graph8.update_graph(new_value_1=yaw_dt, new_value_2=sp_dt_yaw)

    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {data}")

# se creaza obiectul folosit pentru comunicatie si i se atribuie functia de mai sus
network_manager = comunication_control.NetworkManager(on_receive_callback=handle_incoming_data)

def send_pid_vals(reg):
    """Trimite noile valori PID catre Arduino"""
    data = {}
    if reg == "PT1_A":
        #cazul in care trimite alta valoare pt1
        data = {
            "a":pid_vals.a
        }
    else:

        kp = pid_vals.kp
        ki = pid_vals.ki
        kd = pid_vals.kd
        # creaza json-ul necesar transmiterii, 
        # acesta contine valorile propriu zise si regulatorul de care fac parte
        data = {
            "kp": kp,
            "ki": ki,
            "kd": kd,
            "reg":reg
        }
    print(data)
    json_str = json.dumps(data)
    # trimite datele
    network_manager.send_data(json_str)
    print("am trimis")

# se seteaza functia de callback a butoanelor ferestrei de submit
pid_vals.set_external_callback(send_pid_vals)

async def keyboard_loop(kb: KeyboardInput):
    print("Keyboard loop running at 10 Hz. Press ESC to exit.")
    while True:
        kb.update_state()
        state = kb.get_state()
        print(state, end='\r')
        if kb.has_changed():
            network_manager.send_data(kb.to_json())
        #if keyboard.is_pressed('esc'):
        #    print("\nExiting keyboard loop.")
        #    break
        await asyncio.sleep(0.1)  # 10 Hz

async def main():
    kb = KeyboardInput()

    # Start the keyboard loop as an async task (non-blocking)
    keyboard_task = asyncio.create_task(keyboard_loop(kb))

    # Start network receiving as an async task (non-blocking)
    network_task = asyncio.create_task(network_manager.start_receiving())

    try:
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0.016)  # ~60 FPS
    except asyncio.CancelledError:
        pass
    finally:
        print("Shutting down...")

        # Gracefully cancel background tasks
        keyboard_task.cancel()
        network_task.cancel()

        await asyncio.gather(keyboard_task, network_task, return_exceptions=True)

        dpg.destroy_context()

# porneste bucla principala in mod asinron
if __name__ == "__main__":
    asyncio.run(main())
