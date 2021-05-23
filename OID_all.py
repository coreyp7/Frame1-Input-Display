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
    #
    ## VIEW STUFF ##
    on_color = "black"
    off_color = "white"

    test = False
    top = None

    width = 3

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
        """
        self.canvas.create_oval(
            20, 91, 55, 128, outline="black", width=3, fill=self.determine_fill(self.l)
        )

        self.canvas.create_oval(
            62,
            64,
            97,
            101,
            outline="black",
            width=self.width,
            fill=self.determine_fill(self.g_left),
        )"""
        self.redraw_new_inputs()

        self.my_after()

        self.top.mainloop()

    def my_after(self):
        self.redraw_new_inputs()  # Redraw appropriate buttons here
        self.top.after(25, self.my_after)  # Repeat in 75

    def redraw_new_inputs(self):
        new_inputs = self.get_input()

        if new_inputs[0][0] != self.a:  # A BUTTON
            self.a = not self.a
            self.canvas.create_oval(
                406,
                189,
                441,
                226,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.a),
            )

        if new_inputs[0][1] != self.b:  # B BUTTON
            self.b = not self.b
            self.canvas.create_oval(
                417,
                79,
                452,
                116,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.b),
            )

        if new_inputs[0][2] != self.x:  # X BUTTON
            self.x = not self.x
            self.canvas.create_oval(
                461,
                59,
                496,
                96,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.x),
            )

        if new_inputs[0][3] != self.y:  # Y BUTTON
            self.y = not self.y
            self.canvas.create_oval(
                461,
                11,
                496,
                48,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.y),
            )

        if new_inputs[0][4] != self.start:  # START BUTTON
            self.start = not self.start
            self.canvas.create_oval(
                286,
                79,
                321,
                116,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.start),
            )

        if new_inputs[0][5] != self.z:  # Z BUTTON
            self.z = not self.z
            self.canvas.create_oval(
                508,
                64,
                543,
                101,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.z),
            )

        if new_inputs[0][6] != self.r:  # R BUTTON
            self.r = not self.r
            self.canvas.create_oval(
                417,
                31,
                452,
                68,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.r),
            )

        if new_inputs[0][7] != self.l:  # L BUTTON
            self.l = not self.l
            L_button = self.canvas.create_oval(
                20,
                91,
                55,
                128,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.l),
            )

        if new_inputs[0][8] != self.ls1:  # LIGHT SHEILD 1 BUTTON
            self.ls1 = not self.ls1
            self.canvas.create_oval(
                508,
                17,
                543,
                53,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.ls1),
            )

        if new_inputs[0][9] != self.ls2:  # LIGHT SHEILD 2 BUTTON
            self.ls2 = not self.ls2
            self.canvas.create_oval(
                552,
                45,
                587,
                82,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.ls2),
            )

        if new_inputs[1][0] != self.g_up:  # Z BUTTON
            self.g_up = not self.g_up
            self.canvas.create_oval(
                552,
                88,
                587,
                125,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.g_up),
            )

        if new_inputs[1][1] != self.g_down:  # GREYSTICK DOWN
            self.g_down = not self.g_down
            self.canvas.create_oval(
                109,
                59,
                144,
                96,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.g_down),
            )

        if new_inputs[1][2] != self.g_left:  # GREYSTICK LEFT
            self.g_left = not self.g_left
            self.canvas.create_oval(
                62,
                64,
                97,
                101,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.g_left),
            )

        if new_inputs[1][3] != self.g_right:  # GREYSTICK RIGHT
            self.g_right = not self.g_right
            self.canvas.create_oval(
                153,
                79,
                188,
                116,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.g_right),
            )

        if new_inputs[2][0] != self.c_up:  # C-STICK UP
            self.c_up = not self.c_up
            self.canvas.create_oval(
                406,
                139,
                441,
                176,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.c_up),
            )

        if new_inputs[2][1] != self.c_down:  # C-STICK DOWN
            self.c_down = not self.c_down
            self.canvas.create_oval(
                368,
                216,
                403,
                253,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.c_down),
            )

        if new_inputs[2][2] != self.c_left:  # C-STICK LEFT
            self.c_left = not self.c_left
            self.canvas.create_oval(
                368,
                166,
                403,
                203,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.c_left),
            )

        if new_inputs[2][3] != self.c_right:  # C-STICK RIGHT
            self.c_right = not self.c_right
            self.canvas.create_oval(
                443,
                166,
                478,
                203,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.c_right),
            )

        if new_inputs[3][0] != self.mod_x:  # MOD X
            self.mod_x = not self.mod_x
            self.canvas.create_oval(
                165,
                190,
                200,
                227,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.mod_x),
            )

        if new_inputs[3][1] != self.mod_y:  # MOD Y
            self.mod_y = not self.mod_y
            self.canvas.create_oval(
                203,
                215,
                238,
                252,
                outline="black",
                width=self.width,
                fill=self.determine_fill(self.mod_y),
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

    def determine_fill(self, state):
        switcher = {True: self.on_color, False: self.off_color}
        return switcher.get(state, "ERROR")


if __name__ == "__main__":
    exe = OID_all()
    exe.start_exe()

