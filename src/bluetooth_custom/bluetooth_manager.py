import bluetooth
import pexpect
import time
import sys
import os
import gui.gui as g

class Bluetooth_Manager ():

    def __init__(self, gui):
        self.__password = ""
        self.devices = []
        self.devices_connected = []
        self.gui = gui

    def activate_bluetooth(self, event):
        bluetooth_status = self.__execute_command("systemctl status bluetooth").read()

        if not ("active (running)" in bluetooth_status):
            stream = self.__execute_command("systemctl is-enabled bluetooth.service")
            enabled = stream.read()

            if(enabled != "enabled"):
                self.__execute_command_sudo('rfkill unblock bluetooth')
                
            self.__execute_command_sudo('systemctl start bluetooth')

            bluetooth_status = self.__execute_command("systemctl status bluetooth").read()

            if("active (running)" in bluetooth_status):
                print("Bluetooth activated")
            
        else:
            print("Bluetooth is already active")

    def deactivate_bluetooth(self, event):
        self.__execute_command_sudo('systemctl stop bluetooth')
        bluetooth_status = self.__execute_command("systemctl status bluetooth").read()
        if not ("active (running)" in bluetooth_status):
            print("Bluetooth deactivated")

    def scan_bluetooth_devices(self, event):
        bluetooth_status = self.__execute_command('systemctl status bluetooth').read()
        if ("active (running)" in bluetooth_status):
            self.gui.clear_devices()
            self.devices = bluetooth.discover_devices(lookup_names= True, lookup_class= True)
            self.gui.add_devices(self.devices, self.devices_connected, self.connect_to_device, self.disconnect_from_device)
        else:
            self.gui.error('Activate Bluetooth first')

    def connect_to_device(self, device):
        print("Connecting to " + str(device))
        mac_address = device[0]
        command = 'pair' + mac_address




    def disconnect_from_device(self, device):
        print("Disconnecting from " + str(device))

    def __get_password(self):
        password = g.PasswordPrompt(self.gui).show()
        return password

    def __execute_command_sudo(self, command):
        try:
            if(self.__password == ""):
                self.__password = str(self.__get_password())
            status = os.system('echo %s|sudo -S %s' % (self.__password, command))
            return status
        
        except:
            self.gui.error("ERROR: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))

    def __execute_command(self, command):
        try:
            stream = os.popen(command)
            return stream
        
        except:
            self.gui.error("ERROR: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))

    def __execute_bluetoothctl(self, command, pause = 0):
        
        bluetoothctl = pexpect.spawn('bluetoothctl', echo=False)

        time.sleep(pause)

        bluetoothctl.send(command + '\n')

