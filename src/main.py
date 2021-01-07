import sys
import atexit

import gui.gui as g
import bluetooth_custom.bluetooth_manager as btm


gui = g.Gui()
btm = btm.Bluetooth_Manager(gui)

gui.set_button_activate(btm.activate_bluetooth)
gui.set_button_deactivate(btm.deactivate_bluetooth)
gui.set_button_scan(btm.scan_bluetooth_devices)


def cleanup(* args):
    #execute_command_sudo('systemctl stop bluetooth')
    sys.exit(0)

atexit.register(cleanup)

gui.start()
