import os

from tkinter import *


class OID_view:

    on_color = "black"
    off_color = "white"

    def __init__(self):
        top = Tk()

        C = Canvas(top, height=480, width=720)

        C.pack(expand=YES, fill=BOTH)

        cp = os.getcwd()
        # print(cp)
        # cp += "\Frame1-Display\FRAME1_LIGHT_FRONT_LAYOUT.gif"
        # print(cp)

        # Inserting frame1 photo for reference
        img = PhotoImage(file="FRAME1_LIGHT_FRONT_LAYOUT.gif")
        C.create_image(0, 0, anchor=NW, image=img)

        size = 45
        # Width 3 and 4 looks like what I'll go with.
        L_button = C.create_oval(
            20, 91, 55, 128, outline="black", width=3, fill=self.determine_fill(False)
        )

        left_grey_stick = C.create_oval(
            62, 64, 97, 101, outline="black", width=3, fill=self.determine_fill(False)
        )

        top.mainloop()

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

