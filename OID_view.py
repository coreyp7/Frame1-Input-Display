from OID_controller import OID_controller
import os

from tkinter import *


class OID_view:

    on_color = "black"
    off_color = "white"

    test = False
    top = None

    canvas = None

    general_buttons = [
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ]
    grey_stick = [False, False, False, False]
    c_stick = [False, False, False, False]
    mod_buttons = [False, False]

    controller = None

    def __init__(self, controller=OID_controller):
        self.controller = controller

    def start(self):
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
            20, 91, 55, 128, outline="black", width=3, fill=self.determine_fill(False),
        )

        left_grey_stick = self.canvas.create_oval(
            62, 64, 97, 101, outline="black", width=3, fill=self.determine_fill(False),
        )

        self.my_after()

        self.top.mainloop()

    def update_display(self):
        # self.canvas = Canvas(self.top, height=480, width=720)

        # self.canvas.pack(expand=YES, fill=BOTH)

        # Width 3 and 4 looks like what I'll go with.
        L_button = self.canvas.create_oval(
            20,
            91,
            55,
            128,
            outline="black",
            width=3,
            fill=self.determine_fill(self.general_buttons[7]),
        )

        left_grey_stick = self.canvas.create_oval(
            62, 64, 97, 101, outline="black", width=3, fill=self.determine_fill(False),
        )

    def update_input_information(self):
        input = self.controller.get_input_information()
        self.general_buttons = input[0]
        self.grey_stick = input[1]
        self.c_stick = input[2]
        self.mod_buttons = input[3]

    def my_after(self):
        self.update_input_information()
        self.update_display()
        self.top.after(75, self.my_after)

    # scaling test
    """circletest = C.create_oval(122, 128, 194, 200, outline="black", width=4)
    circle = C.create_oval(40, 182, 110, 256, outline="black", width=3)"""

    # Given True/False (corresponding to button activity), this will return the
    # correct color for the button to fill. Fake Switch Statement.
    # state: is the button on or off? True or False?
    # on_color and off_color: pass respective variables from self
    def determine_fill(self, state):
        switcher = {True: self.on_color, False: self.off_color}
        return switcher.get(state, "ERROR")

