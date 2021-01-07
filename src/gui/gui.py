import tkinter as tk

#https://realpython.com/python-gui-tkinter/#displaying-clickable-buttons-with-button-widgets

class Gui(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)

        self.rowconfigure(0, weight = 1, minsize = 20)
        self.rowconfigure(1, weight = 1, minsize = 180)

        self.columnconfigure(0, weight = 1, minsize = 300)


        #------------------------------------------------------------------------------


        self.header = tk.Frame(bg = "grey", width = "750", height = "50", master = self)
        self.header.grid(row = 0, column = 0, sticky = "nsew")


        #------------------------------------------------------------------------------


        self.body = tk.Frame(bg = "green", width = "750", height = "450", master = self)
        self.body.grid(row = 1, column = 0, sticky = "nsew")

        self.body.rowconfigure(0, weight = 1, minsize = 200)
        self.body.columnconfigure(0, weight = 1, minsize = 100)



        self.button_frame = tk.Frame(master=self.body, bg="black", width = "250", height = "450")
        self.button_frame.grid(row = 0, column = 0, sticky = "nsew")

        for i in range(0, 2):
            self.button_frame.rowconfigure(i, weight = 1, minsize = 20)

        self.button_frame.rowconfigure(2, weight = 8, minsize = 160)
        self.button_frame.columnconfigure(0, weight = 1, minsize = 100)

        self.button_activate = tk.Button(text = "Activate Bluetooth", master=self.button_frame)
        self.button_activate.grid(row = 0, column = 0, sticky = "nsew")

        self.button_deactivate = tk.Button(text = "Deactivate Bluetooth", master=self.button_frame)
        self.button_deactivate.grid(row = 1, column = 0, sticky = "nsew")

        self.button_scan = tk.Button(text = "Scan", master=self.button_frame)
        self.button_scan.grid(row = 2, column = 0, sticky = "nsew")

        self.button_field_filler = tk.Frame(master = self.button_frame, bg = "yellow", width = "250", height = "340")
        self.button_field_filler.grid(row = 3, column = 0, sticky = "nsew")



        self.body.columnconfigure(1, weight = 2, minsize = 200)

        self.frame_devices= tk.Frame(master=self.body, bg = "red", width = "500", height = "450")
        self.frame_devices.grid(row = 0, column = 1, sticky = "nsew")

        self.frame_devices_children = []
        self.frame_devices_connected_children = []

        #------------------------------------------------------------------------------

    def error(self, message = "There was an error"):
        error_window = tk.Toplevel(self, bg = "black")

        error_window.title("Error")

        label = tk.Label(master = error_window, fg = "white", bg = "black", text = message)
        label.pack(padx = 10, pady = 15)

    def start(self):

        self.mainloop()

    def set_button_activate(self, activate_bluetooth):
        self.button_activate.bind("<Button-1>", activate_bluetooth)

    def set_button_deactivate(self, deactivate_bluetooth):
        self.button_deactivate.bind("<Button-1>", deactivate_bluetooth)

    def set_button_scan(self, scan_bluetooth_devices):
        self.button_scan.bind("<Button-1>", scan_bluetooth_devices)

    def add_devices(self, devices, devices_connected, connect, disconnect):
        self.frame_devices_children = [len(devices)]
        for i in range(0, len(devices)):
            self.frame_devices_children[i] = Frame_Device(self.frame_devices, devices[i], i, connect)
        self.frame_devices_connected_children = [len(devices_connected)]
        for i in range(0, len(devices_connected)):
            self.frame_devices_connected_children[i] = Frame_Device_Connected(self.frame_devices_connected, devices_connected[i], i, disconnect)
            
    
    def clear_devices(self):
        for element in self.frame_devices.grid_slaves():
            element.destroy()
        self.frame_devices_children = []
        self.frame_devices_connected_children = []



class PasswordPrompt(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.var = tk.StringVar()

        self.label = tk.Label(self, text="Sudo Password:")
        self.password_entry = tk.Entry(self, textvariable = self.var, show='*', fg = "white", bg = "black", width = "60")
        self.button = tk.Button(self, text = "Ok", command = self.on_ok)

        self.label.pack(side="top", fill="x")
        self.password_entry.pack(side="top", fill="x")
        self.button.pack(side="right")

        self.password_entry.bind("<Return>", self.on_ok)

    def on_ok(self, event = None):
        self.destroy()

    def show(self):

        self.wm_deiconify()
        self.focus_force()
        self.wait_window()
        return self.var.get()



class Frame_Device():

    def __init__(self, master, device, i, connect):

        self.frame = tk.Frame(master = master)
        self.frame.grid(row = i, column = 0, sticky = "nsew")

        self.frame.columnconfigure(0, weight = 3, minsize = 150)
        self.frame.columnconfigure(1, weight = 1, minsize = 50)

        self.label = tk.Label(master = self.frame, text = device)
        self.label.grid(row = 0, column = 0, sticky = "nsew")

        self.button = tk.Button(master = self.frame, text = "Connect", command = lambda: connect(device))
        self.button.grid(row = 0, column = 1, sticky = "nsew")



class Frame_Device_Connected():

    def __init__(self, master, device, i, disconnect):

        self.frame = tk.Frame(master = master)
        self.frame.grid(row = i, column = 0, sticky = "nsew")

        self.frame.columnconfigure(0, weight = 3, minsize = 150)
        self.frame.columnconfigure(1, weight = 1, minsize = 50)

        self.label = tk.Label(master = self.frame, text = device)
        self.label.grid(row = 0, column = 0, sticky = "nsew")

        self.button = tk.Button(master = self.frame, text = "Disconnect", command = lambda:disconnect(device))
        self.button.grid(row = 0, column = 1, sticky = "nsew")