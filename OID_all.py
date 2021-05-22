import joystickapi
import msvcrt
import time
import os
from tkinter import *


class OID_all:
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
    #
    ## VIEW STUFF ##
    on_color = "black"
    off_color = "white"

    test = False
    top = None

    canvas = None
    ################

    def __init__(self):
        print("start")

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

    def start_exe(self):
        self.top = Tk()

        self.canvas = Canvas(self.top, height=480, width=720)

        self.canvas.pack(expand=YES, fill=BOTH)

        cp = os.getcwd()
        # print(cp)
        # cp += "\Frame1-Display\FRAME1_LIGHT_FRONT_LAYOUT.gif"
        # print(cp)

        # Inserting frame1 photo for reference
        img = PhotoImage(file="FRAME1_LIGHT_FRONT_LAYOUT.gif")
        self.canvas.create_image(0, 0, anchor=NW, image=img)

        size = 45
        # Width 3 and 4 looks like what I'll go with.
        L_button = self.canvas.create_oval(
            20, 91, 55, 128, outline="black", width=3, fill=self.determine_fill(self.l)
        )

        self.my_after()

        self.top.mainloop()

    def my_after(self):
        self.redraw_new_inputs()  # Redraw appropriate buttons here
        self.top.after(50, self.my_after)  # Repeat in 75

    def redraw_new_inputs(self):
        new_inputs = self.get_input()
        if new_inputs[0][7] != self.l:
            self.l = not self.l
            L_button = self.canvas.create_oval(
                20,
                91,
                55,
                128,
                outline="black",
                width=3,
                fill=self.determine_fill(self.l),
            )
        # else:  # do this for every other of the 19 buttons

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

        # set light sheild buttons back in general_buttons
        if rotation[0] > 12543:
            general_buttons.append(False)
            general_buttons.append(True)
        elif rotation[0] > 0:
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

    def determine_fill(self, state):
        switcher = {True: self.on_color, False: self.off_color}
        return switcher.get(state, "ERROR")


if __name__ == "__main__":
    exe = OID_all()
    exe.start_exe()

