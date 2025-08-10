# GitLicenta
Complete code of the ESP32 Flight controller including the Python debug interface.

Clone the repo localy, Flight_Controller folder is to be flashed on the ESP32 using ArduinoIDE and the Interfata_Python folder is the Python code. You must first install the requirements.

To make it connect via Bluetooth you must first find the MAC address of your DualSense controller and replace the one in the Config.h file. For LAN connection you need to insert the login credentials in the same file at the correct field. The last step is to insert the local IP of the device that runs the Python app in the same Config.h file the compile and write the program.

In the Python app files is a config.py file that has a IP field for the ESP32 local IP. The drones IP will be printed in the serial monitor in the first few seconds of run.

Now the 2 should be connected and the Python app can be used to monitor and change regulator constants.
