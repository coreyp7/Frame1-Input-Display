import tkinter
import joystickapi
import msvcrt
import time
import os

# from tkinter import *
import pickle
from tkinter import (
    Spinbox,
    Tk,
    Label,
    Button,
    ttk,
    Toplevel,
    Entry,
    Menu,
    font,
    Radiobutton,
    Scrollbar,
    Listbox,
    Checkbutton,
    Frame,
    YES,
    NO,
    BOTH,
    Canvas,
    colorchooser,
)


class Frame1_Input_Display:
    ret = False
    caps = None
    startInfo = None
    num = 0
    id = None
    last_input = []
    #
    a = False
    b = False
    x = False
    y = False
    start = False
    z = False
    r = False
    l = False
    ls1 = False
    ls2 = False

    g_up = False
    g_down = False
    g_left = False
    g_right = False

    c_up = False
    c_down = False
    c_left = False
    c_right = False

    mod_x = False
    mod_y = False

    rotation_positive = True

    a_button_display = None
    #
    ## VIEW STUFF ##
    top = None
    canvas = None

    # test = False
    # Button Details
    width = 3
    # on_color = "white"
    on_color = "#FFFFFF"
    off_color = "#000000"
    outline = "#FFFFFF"
    background = "#000000"

    resizeable = False

    set_res = "600x276"

    scale = 1

    boot_warning = True

    # window_width
    # window_height
    ################

    # a subclass of Canvas for dealing with resizing of windows

    def save(self):
        final_dump = [
            self.width,
            self.set_res,
            self.scale,
            self.boot_warning,
            self.on_color,
            self.off_color,
            self.outline,
            self.background,
            self.resizeable,
        ]
        pickle_file = open("config.txt", "wb")
        pickle_file.truncate(0)
        pickle.dump(final_dump, pickle_file)

    def load(self):
        load = pickle.load(open("config.txt", "rb"))
        self.width = load[0]
        self.set_res = load[1]
        self.window_width = self.set_res.split("x")[0]
        self.window_height = self.set_res.split("x")[1]
        self.scale = load[2]
        self.boot_warning = load[3]
        self.on_color = load[4]
        self.off_color = load[5]
        self.outline = load[6]
        self.background = load[7]
        self.resizeable = load[8]

    def __init__(self):
        print("start")

        try:
            self.load()
        except:
            print("No previous settings.")
            self.window_width = 600
            self.window_height = 276
            self.scale = 1
            pass

        if self.boot_warning:
            self.boot_warning_window()

        self.num = joystickapi.joyGetNumDevs()
        self.ret, self.caps, self.startinfo = False, None, None
        for id in range(self.num):
            self.ret, self.caps = joystickapi.joyGetDevCaps(id)
            if self.ret:
                print("gamepad detected: " + self.caps.szPname)
                self.ret, self.startinfo = joystickapi.joyGetPosEx(id)
                self.id = id
                break
        else:
            print("no gamepad detected")
            self.no_frame1_window()
            exit(1)

        # NOTE: have to wait a second for some reason to allow for proper calibration of roation_positive.
        time.sleep(0.5)

        # NOTE: Here is where I check what the fuck is up with rotation.
        self.ret, self.info = joystickapi.joyGetPosEx(self.id)
        if self.ret:
            btns = [
                (1 << i) & self.info.dwButtons != 0
                for i in range(self.caps.wNumButtons)
            ]
            axisXYZ = [
                self.info.dwXpos - self.startinfo.dwXpos,
                self.info.dwYpos - self.startinfo.dwYpos,
                self.info.dwZpos - self.startinfo.dwZpos,
            ]
            axisRUV = [
                self.info.dwRpos - self.startinfo.dwRpos,
                self.info.dwUpos - self.startinfo.dwUpos,
                self.info.dwVpos - self.startinfo.dwVpos,
            ]
            formatted_input_info = btns, axisXYZ, axisRUV
            rotation = formatted_input_info[2]

            # Here we finally set the rotation_positive variable (calibration).
            # As far as I know, these are the only two that exist.
            """ rotation_positive = True:
                None: [0, 0, 0], [0, 0, 0])
                R: [0, 0, 0], [57599, 0, 0])
                ls1: [0, 0, 0], [12543, 0, 0])
                ls2: [0, 0, 0], [24063, 0, 0])

                rotation_positive = False:
                None: [0, 0, 0], [-24831, 0, 0])
                R:  [0, 0, 0], [32768, 0, 0])
                ls1:  [0, 0, 0], [-12288, 0, 0])
                ls2: [0, 0, 0], [-768, 0, 0]) """
            if rotation[0] == 0:
                self.rotation_positive = True
            else:
                self.rotation_positive = False

    def colors_window(self):
        win = tkinter.Toplevel()
        win.configure(background=self.background)
        win.wm_title("Options: Settings")
        win.geometry("500x300")
        win.resizable(width=False, height=False)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        frame = Frame(win, bg=self.background)
        frame.grid(column=0, row=0)

        def choose_color_on_color():
            color_code = colorchooser.askcolor(title='Choose "Button Press"color:')
            if color_code[1] == None:
                win.destroy()
            else:
                self.on_color = color_code[1]
                # win.destroy()
                self.top.destroy()
                self.start_exe()

        def off_color():
            color_code = colorchooser.askcolor(title='Choose "Button Press"color:')
            if color_code[1] == None:
                win.destroy()
            else:
                self.off_color = color_code[1]
                # win.destroy()
                self.top.destroy()
                self.start_exe()

        def outline_color():
            color_code = colorchooser.askcolor(title='Choose "Button Press"color:')
            if color_code[1] == None:
                win.destroy()
            else:
                self.outline = color_code[1]
                # win.destroy()
                self.top.destroy()
                self.start_exe()

        def background_color():
            color_code = colorchooser.askcolor(title='Choose "Button Press"color:')
            if color_code[1] == None:
                win.destroy()
            else:
                self.background = color_code[1]
                # win.destroy()
                self.top.destroy()
                self.start_exe()

        color_code_button = Button(
            frame,
            command=choose_color_on_color,
            text='Change "Button Press" Color',
            bg="#000000",
            fg="#FFFFFF",
        )
        color_code_button.grid(row=0, column=0)

        off_color_button = Button(
            frame,
            command=off_color,
            text='Change "Button Off" Color',
            bg="#000000",
            fg="#FFFFFF",
        )
        off_color_button.grid(row=1, column=0)

        outline_color_button = Button(
            frame,
            command=outline_color,
            text="Change Outline Color",
            bg="#000000",
            fg="#FFFFFF",
        )
        outline_color_button.grid(row=2, column=0)

        bg_color_button = Button(
            frame,
            command=background_color,
            text="Change Background Color",
            bg="#000000",
            fg="#FFFFFF",
        )
        bg_color_button.grid(row=3, column=0)

    def start_exe(self):

        self.top = Tk()
        self.top.title("Frame1 Display")
        # self.top.bind("<Configure>", self.on_resize)
        # self.top.resizable(False, False)
        self.frame = Frame(self.top, width=self.window_width, height=self.window_height)
        self.frame.pack(fill=BOTH, expand=YES)
        # Checking for if the window is resizable.
        if self.resizeable:
            self.top.resizable(True, True)
        else:
            self.top.resizable(False, False)

        # ResizingCanvas created here
        self.canvas = ResizingCanvas(
            self.frame,
            height=self.window_height,
            width=self.window_width,
            background=self.background,
            highlightthickness=0,
        )
        # self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.pack(expand=YES, fill=BOTH)
        # self.canvas.bind("<Configure>", self.on_resize)

        # Menubar stuff
        menubar = Menu(self.top, bg=self.background, fg="white")
        self.top.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0, bg="white", fg="black")
        file_menu.add_command(label="Settings", command=self.settings_window)
        file_menu.add_command(label="Colors", command=self.colors_window)
        file_menu.add_command(label="Save Current Settings", command=self.save)

        menubar.add_cascade(label="Options", menu=file_menu)

        self.instantiate_ovals()

        self.canvas.addtag_all("all")

        self.my_after()

        self.top.mainloop()

    def settings_window(self):
        win = tkinter.Toplevel()
        win.configure(background=self.background)
        win.wm_title("Options: Settings")
        win.geometry("500x300")
        win.resizable(width=False, height=False)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=2)
        # win.columnconfigure(1, weight=1)
        win.rowconfigure(1, weight=2)
        win.rowconfigure(2, weight=0)

        topframe = Frame(win, bg=self.background)
        topframe.grid(column=0, row=0)
        middleframe = Frame(win, bg=self.background)
        middleframe.grid(column=0, row=1)
        bottomframe = Frame(win, bg=self.background)
        bottomframe.grid(column=0, row=2)

        ### top frame

        width_label = Label(
            topframe,
            text="Outline thickness:",
            fg="#FFFFFF",
            bg="#000000",
            font="TkDefaultFont 12",
        )
        width_label.grid(row=0, column=0)

        width_spin_var = tkinter.StringVar()
        width_spin_var.set(str(self.outline))
        width_spinbox = Spinbox(
            topframe,
            from_=1,
            to=5,
            textvariable=width_spin_var,
            state="readonly",
            width=5,
        )
        width_spinbox.grid(row=0, column=1)

        base_resolution_label = Label(
            topframe,
            text="Base Resolution:",
            fg="#FFFFFF",
            bg="#000000",
            font="TkDefaultFont 12",
        )
        base_resolution_label.grid(row=1, column=0)

        base_resolution_var = tkinter.StringVar()

        base_resolution_combo = ttk.Combobox(
            topframe, state="readonly", textvariable=base_resolution_var, width=10
        )
        base_resolution_combo["values"] = ["600x276", "900x414", "1200x552"]
        for i in base_resolution_combo["values"]:
            if i == self.set_res:
                base_resolution_combo.current(base_resolution_combo["values"].index(i))
        base_resolution_combo.grid(row=1, column=1)

        ### middle frame
        lock_window_var = tkinter.BooleanVar()
        Checkbutton(
            middleframe,
            text="Lock Window Size",
            variable=lock_window_var,
            fg="#FFFFFF",
            bg="#000000",
            onvalue=False,
            offvalue=True,
            selectcolor=self.background,
            activeforeground=self.background,
        ).grid(row=0, column=0)

        boot_warning_var = tkinter.BooleanVar()
        Checkbutton(
            middleframe,
            text="Wait for user confirmation on launch (intro window)",
            variable=boot_warning_var,
            fg="#FFFFFF",
            bg="#000000",
            onvalue=True,
            offvalue=False,
            selectcolor=self.background,
            activeforeground=self.background,
        ).grid(row=1, column=0)

        ### OK and CANCEL buttons - bottom frame
        def change_and_close_window():
            self.width = width_spinbox.get()
            self.resizeable = lock_window_var.get()
            self.window_width = base_resolution_var.get().split("x")[0]
            self.window_height = base_resolution_var.get().split("x")[1]
            # This is dumb and messy, but this properly sets the scaling
            # depending on the resolution. Goes by place in array.
            if base_resolution_combo["values"].index(base_resolution_var.get()) == 0:
                self.scale = 1
            elif base_resolution_combo["values"].index(base_resolution_var.get()) == 1:
                self.scale = 1.5
            elif base_resolution_combo["values"].index(base_resolution_var.get()) == 2:
                self.scale = 2
            self.set_res = base_resolution_var.get()
            self.boot_warning = boot_warning_var.get()
            ##
            self.top.destroy()
            self.start_exe()

        ok_button = Button(
            bottomframe,
            text="Ok",
            command=change_and_close_window,
            bg=self.background,
            fg=self.on_color,
        )
        ok_button.grid(row=0, column=0)

    def no_frame1_window(self):
        self.top = Tk()
        self.top.configure(background=self.background)
        self.top.wm_title("No Frame1 :(")
        self.top.geometry("500x300")
        self.top.resizable(width=False, height=False)
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        # win.columnconfigure(1, weight=1)
        frame = Frame(self.top, bg=self.background)
        frame.grid(column=0, row=0)

        width_label = Label(
            frame,
            text="Frame1 was not detected.\n\nMake sure there are no other controllers plugged in and try again.\n",
            fg=self.outline,
            bg=self.background,
            font="TkDefaultFont 12",
        )
        width_label.grid(row=0, column=0)
        self.top.mainloop()

    def boot_warning_window(self):
        self.top = Tk()
        self.top.configure(background=self.background)
        self.top.wm_title("Warning")
        self.top.geometry("500x300")
        self.top.resizable(width=False, height=False)
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        # self.top.columnconfigure(1, weight=1)
        frame = Frame(self.top, bg=self.background)
        frame.grid(column=0, row=0)
        frame.rowconfigure(1, weight=1)
        width_label = Label(
            frame,
            text="Make sure no other controllers are plugged in to continue.\n\nPress 'Ok' when you're ready to detect your Frame1.",
            fg=self.outline,
            bg=self.background,
            font="TkDefaultFont 12",
        )
        width_label.grid(row=0, column=0)
        ok_button = Button(
            frame,
            text="Ok",
            command=self.top.destroy,
            bg=self.background,
            fg=self.on_color,
        )
        ok_button.grid(row=1, column=0)
        self.top.mainloop()

    def my_after(self):
        self.redraw_new_inputs()  # Redraw appropriate buttons here
        # print(self.canvas.height, self.canvas.width)
        self.top.after(25, self.my_after)  # Repeat in 75

    def instantiate_ovals(self):
        self.a_button_display = self.canvas.create_oval(  # A BUTTON
            406 * self.scale,
            189 * self.scale,
            441 * self.scale,
            226 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.a),
        )

        self.b_button_display = self.canvas.create_oval(  # B BUTTON
            417 * self.scale,
            79 * self.scale,
            452 * self.scale,
            116 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.b),
        )

        self.x_button_display = self.canvas.create_oval(  # X BUTTON
            461 * self.scale,
            59 * self.scale,
            496 * self.scale,
            96 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.x),
        )

        self.y_button_display = self.canvas.create_oval(  # Y BUTTON
            461 * self.scale,
            11 * self.scale,
            496 * self.scale,
            48 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.y),
        )

        self.start_button_display = self.canvas.create_oval(  # START BUTTON
            286 * self.scale,
            79 * self.scale,
            321 * self.scale,
            116 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.start),
        )

        self.z_button_display = self.canvas.create_oval(  # Z BUTTON
            508 * self.scale,
            64 * self.scale,
            543 * self.scale,
            101 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.z),
        )

        self.r_button_display = self.canvas.create_oval(  # R BUTTON
            417 * self.scale,
            31 * self.scale,
            452 * self.scale,
            68 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.r),
        )

        self.l_button_display = self.canvas.create_oval(  # L BUTTON
            20 * self.scale,
            91 * self.scale,
            55 * self.scale,
            128 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.l),
        )

        self.ls1_button_display = self.canvas.create_oval(  # LS1 BUTTON
            508 * self.scale,
            17 * self.scale,
            543 * self.scale,
            53 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.ls1),
        )

        self.ls2_button_display = self.canvas.create_oval(  # LS2 BUTTON
            552 * self.scale,
            45 * self.scale,
            587 * self.scale,
            82 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.ls2),
        )

        self.g_up_button_display = self.canvas.create_oval(  # GREYSTICK UP
            552 * self.scale,
            88 * self.scale,
            587 * self.scale,
            125 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.g_up),
        )

        self.g_down_button_display = self.canvas.create_oval(  # GREYSTICK DOWN
            109 * self.scale,
            59 * self.scale,
            144 * self.scale,
            96 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.g_down),
        )

        self.g_left_button_display = self.canvas.create_oval(  # GREYSTICK LEFT
            62 * self.scale,
            64 * self.scale,
            97 * self.scale,
            101 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.g_left),
        )

        self.g_right_button_display = self.canvas.create_oval(  # GREYSTICK RIGHT
            153 * self.scale,
            79 * self.scale,
            188 * self.scale,
            116 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.g_right),
        )

        self.c_up_button_display = self.canvas.create_oval(  # CSTICK UP
            406 * self.scale,
            139 * self.scale,
            441 * self.scale,
            176 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.c_up),
        )

        self.c_down_button_display = self.canvas.create_oval(  # CSTICK DOWN
            368 * self.scale,
            216 * self.scale,
            403 * self.scale,
            253 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.c_down),
        )

        self.c_left_button_display = self.canvas.create_oval(  # CSTICK LEFT
            368 * self.scale,
            166 * self.scale,
            403 * self.scale,
            203 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.c_left),
        )

        self.c_right_button_display = self.canvas.create_oval(  # CSTICK RIGHT
            443 * self.scale,
            166 * self.scale,
            478 * self.scale,
            203 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.c_right),
        )

        self.mod_x_button_display = self.canvas.create_oval(  # MOD X
            165 * self.scale,
            190 * self.scale,
            200 * self.scale,
            227 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.mod_x),
        )

        self.mod_y_button_display = self.canvas.create_oval(  # MOD Y
            203 * self.scale,
            215 * self.scale,
            238 * self.scale,
            252 * self.scale,
            outline=self.outline,
            width=self.width,
            fill=self.determine_fill(self.mod_y),
        )

    def redraw_new_inputs(self):
        new_inputs = self.get_input()

        if new_inputs[0][0] != self.a:  # A BUTTON
            self.a = not self.a
            # use variable of shape (initially instantiated in some startup function) to change fill. Check bookmarked resources.
            self.canvas.itemconfig(
                self.a_button_display, fill=self.determine_fill(self.a)
            )

        if new_inputs[0][1] != self.b:  # B BUTTON
            self.b = not self.b
            self.canvas.itemconfig(
                self.b_button_display, fill=self.determine_fill(self.b)
            )

        if new_inputs[0][2] != self.x:  # X BUTTON
            self.x = not self.x
            self.canvas.itemconfig(
                self.x_button_display, fill=self.determine_fill(self.x)
            )

        if new_inputs[0][3] != self.y:  # Y BUTTON
            self.y = not self.y
            self.canvas.itemconfig(
                self.y_button_display, fill=self.determine_fill(self.y)
            )

        if new_inputs[0][4] != self.start:  # START BUTTON
            self.start = not self.start
            self.canvas.itemconfig(
                self.start_button_display, fill=self.determine_fill(self.start)
            )

        if new_inputs[0][5] != self.z:  # Z BUTTON
            self.z = not self.z
            self.canvas.itemconfig(
                self.z_button_display, fill=self.determine_fill(self.z)
            )

        if new_inputs[0][6] != self.r:  # R BUTTON
            self.r = not self.r
            self.canvas.itemconfig(
                self.r_button_display, fill=self.determine_fill(self.r)
            )

        if new_inputs[0][7] != self.l:  # L BUTTON
            self.l = not self.l
            self.canvas.itemconfig(
                self.l_button_display, fill=self.determine_fill(self.l)
            )

        if new_inputs[0][8] != self.ls1:  # LIGHT SHEILD 1 BUTTON
            self.ls1 = not self.ls1
            self.canvas.itemconfig(
                self.ls1_button_display, fill=self.determine_fill(self.ls1)
            )

        if new_inputs[0][9] != self.ls2:  # LIGHT SHEILD 2 BUTTON
            self.ls2 = not self.ls2
            self.canvas.itemconfig(
                self.ls2_button_display, fill=self.determine_fill(self.ls2)
            )

        if new_inputs[1][0] != self.g_up:  # Z BUTTON
            self.g_up = not self.g_up
            self.canvas.itemconfig(
                self.g_up_button_display, fill=self.determine_fill(self.g_up)
            )

        if new_inputs[1][1] != self.g_down:  # GREYSTICK DOWN
            self.g_down = not self.g_down
            self.canvas.itemconfig(
                self.g_down_button_display, fill=self.determine_fill(self.g_down)
            )

        if new_inputs[1][2] != self.g_left:  # GREYSTICK LEFT
            self.g_left = not self.g_left
            self.canvas.itemconfig(
                self.g_left_button_display, fill=self.determine_fill(self.g_left)
            )

        if new_inputs[1][3] != self.g_right:  # GREYSTICK RIGHT
            self.g_right = not self.g_right
            self.canvas.itemconfig(
                self.g_right_button_display, fill=self.determine_fill(self.g_right)
            )

        if new_inputs[2][0] != self.c_up:  # C-STICK UP
            self.c_up = not self.c_up
            self.canvas.itemconfig(
                self.c_up_button_display, fill=self.determine_fill(self.c_up)
            )

        if new_inputs[2][1] != self.c_down:  # C-STICK DOWN
            self.c_down = not self.c_down
            self.canvas.itemconfig(
                self.c_down_button_display, fill=self.determine_fill(self.c_down)
            )

        if new_inputs[2][2] != self.c_left:  # C-STICK LEFT
            self.c_left = not self.c_left
            self.canvas.itemconfig(
                self.c_left_button_display, fill=self.determine_fill(self.c_left)
            )

        if new_inputs[2][3] != self.c_right:  # C-STICK RIGHT
            self.c_right = not self.c_right
            self.canvas.itemconfig(
                self.c_right_button_display, fill=self.determine_fill(self.c_right)
            )

        if new_inputs[3][0] != self.mod_x:  # MOD X
            self.mod_x = not self.mod_x
            self.canvas.itemconfig(
                self.mod_x_button_display, fill=self.determine_fill(self.mod_x)
            )

        if new_inputs[3][1] != self.mod_y:  # MOD Y
            self.mod_y = not self.mod_y
            self.canvas.itemconfig(
                self.mod_y_button_display, fill=self.determine_fill(self.mod_y)
            )

    def get_input(self):
        self.ret, self.info = joystickapi.joyGetPosEx(self.id)
        if self.ret:
            btns = [
                (1 << i) & self.info.dwButtons != 0
                for i in range(self.caps.wNumButtons)
            ]
            axisXYZ = [
                self.info.dwXpos - self.startinfo.dwXpos,
                self.info.dwYpos - self.startinfo.dwYpos,
                self.info.dwZpos - self.startinfo.dwZpos,
            ]
            axisRUV = [
                self.info.dwRpos - self.startinfo.dwRpos,
                self.info.dwUpos - self.startinfo.dwUpos,
                self.info.dwVpos - self.startinfo.dwVpos,
            ]

            formatted_input_info = btns, axisXYZ, axisRUV
            # print(formatted_input_info)
            formatted_input_info = self.format_input(formatted_input_info)
            # print(formatted_input_info)
            return formatted_input_info

    def format_input(self, input):

        grey_stick = [False, False, False, False]  # Up, Down, Left, Right
        c_stick = [False, False, False, False]  # Up, Down, Left, Right

        # Just setting linear buttons to their value from param input here
        general_buttons = [
            input[0][0],
            input[0][1],
            input[0][2],
            input[0][3],
            input[0][4],
            input[0][12],
            input[0][13],
            input[0][14],
        ]
        # These are a little more complicated, so storing here for operations.
        axis = input[1]  # [ RIGHT/LEFT, UP/DOWN, nothing ]
        rotation = input[2]  # [ LS1&2, CSTICK UP/DOWN, nothing ]

        mod_buttons = [self.modx_check(axis), self.mody_check(axis)]

        # get grey stick buttons
        if axis[0] > 0:
            grey_stick[3] = True
        elif axis[0] < 0:
            grey_stick[2] = True

        if axis[1] > 0:
            grey_stick[0] = True
        elif axis[1] < 0:
            grey_stick[1] = True

        # get c stick buttons
        if axis[2] > 0:
            c_stick[3] = True
        elif axis[2] < 0:
            c_stick[2] = True

        if rotation[1] > 0:
            c_stick[0] = True
        elif rotation[1] < 0:
            c_stick[1] = True

        # For when wavedashing right with modx
        if axis[0] == 15084 and axis[1] == -6400:
            mod_buttons[0] = True

        # For when wavedashing left with modx
        if axis[0] == -15104 and axis[1] == -6400:
            mod_buttons[0] = True

        # This is to keep modx on when wavedashing (Otherwise, it will flicker off)
        if axis[0] == 13004 and axis[1] == -7680:
            mod_buttons[0] = True
        if axis[0] == -13056 and axis[1] == -7680:
            mod_buttons[0] = True

        # This is to keep mody on when wavedashing (Otherwise, it will flicker off)
        if axis[0] == 10143 and axis[1] == -17407:
            mod_buttons[1] = True
        if axis[0] == -10240 and axis[1] == -17407:
            mod_buttons[1] = True

        # This is to check for up/left and up/right with modx. (It works with mody for some reason)
        if axis[0] == 15084 and axis[1] == 6242:
            mod_buttons[0] = True
        if axis[0] == -15104 and axis[1] == 6242:
            mod_buttons[0] = True

        # set light sheild buttons back in general_buttons (NOTE: adding elements)
        """if rotation[0] > 12543:
            general_buttons.append(False)
            general_buttons.append(True)"""
        if self.rotation_positive:
            if rotation[0] == 24063:
                general_buttons.append(False)
                general_buttons.append(True)
            elif rotation[0] == 12543:
                general_buttons.append(True)
                general_buttons.append(False)
            else:
                general_buttons.append(False)
                general_buttons.append(False)
        else:
            if rotation[0] == -768:
                general_buttons.append(False)
                general_buttons.append(True)
            elif rotation[0] == -12288:
                general_buttons.append(True)
                general_buttons.append(False)
            else:
                general_buttons.append(False)
                general_buttons.append(False)

        final_formatted_input = [general_buttons, grey_stick, c_stick, mod_buttons]

        return final_formatted_input

    def modx_check(self, axis):
        return self.vertical_modx_check(axis[1]) or self.horizontal_modx_check(axis[0])

    def mody_check(self, axis):
        return self.vertical_mody_check(axis[1]) or self.horizontal_mody_check(axis[0])

    # must give this a value only
    def vertical_modx_check(self, val):
        if abs(val) == 10923 or abs(val) == 11008:
            return True
        return False

    # must give this a value only
    def vertical_mody_check(self, val):
        if abs(val) == 15084 or abs(val) == 15104:
            return True
        return False

    # must give this a value only
    def horizontal_modx_check(self, val):
        if abs(val) == 13524 or abs(val) == 13568:
            return True
        return False

    # must give this a value only
    def horizontal_mody_check(self, val):
        if abs(val) == 6762 or abs(val) == 6912:  # if abs(val) == (6762 or 6912):
            return True
        return False

    # Param: Boolean Value
    # Returns: a string representing a color depending on the given param
    def determine_fill(self, state):
        switcher = {True: self.on_color, False: self.off_color}
        return switcher.get(state, "ERROR")


# TEMPORARY SOLUTION FROM INTERNET
# Will be natively integrated in Frame1_Display or will be abandoned
# for strict resolutions for display integrity.
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)


"""
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)
"""

if __name__ == "__main__":
    exe = Frame1_Input_Display()
    exe.start_exe()

