import joystickapi
import msvcrt
import time

class OID_model:

    def start_normal_operation(self):

        print("start")

        num = joystickapi.joyGetNumDevs()
        ret, caps, startinfo = False, None, None
        for id in range(num):
            ret, caps = joystickapi.joyGetDevCaps(id)
            if ret:
                print("gamepad detected: " + caps.szPname)
                ret, startinfo = joystickapi.joyGetPosEx(id)
                break
        else:
            print("no gamepad detected")

        run = ret
        while run:
            time.sleep(0.05)
            if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():  # detect ESC
                run = False

            ret, info = joystickapi.joyGetPosEx(id)
            if ret:
                btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
                axisXYZ = [
                    info.dwXpos - startinfo.dwXpos,
                    info.dwYpos - startinfo.dwYpos,
                    info.dwZpos - startinfo.dwZpos,
                ]
                axisRUV = [
                    info.dwRpos - startinfo.dwRpos,
                    info.dwUpos - startinfo.dwUpos,
                    info.dwVpos - startinfo.dwVpos,
                ]
                
                formatted_input_info = btns, axisXYZ, axisRUV
                #print(formatted_input_info)
                formatted_input_info = self.format_input(formatted_input_info)
                #print(formatted_input_info)
                self.display_nice(formatted_input_info)

    def format_input(self, input):

        grey_stick = [False, False, False, False] # Up, Down, Left, Right
        c_stick = [False, False, False, False] # Up, Down, Left, Right

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
        axis = input[1] # [ RIGHT/LEFT, UP/DOWN, nothing ]
        rotation = input[2] # [ LS1&2, CSTICK UP/DOWN, nothing ]

        mod_buttons = [
            self.modx_check(axis),
            self.mody_check(axis)
        ]
        
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
    def vertical_modx_check(val):
        if abs(val) == 10923 or abs(val) == 11008:
            return True
        return False

    # must give this a value only
    def vertical_mody_check(val):
        if abs(val) == 15084 or abs(val) == 15104:
            return True
        return False

    # must give this a value only
    def horizontal_modx_check(val):
        if abs(val) == 13524 or abs(val) == 13568:
            return True
        return False

    # must give this a value only
    def horizontal_mody_check(val):
        if abs(val) == 6762 or abs(val) == 6912: # if abs(val) == (6762 or 6912):
            return True
        return False

    def display_nice(var):
        if var[0][0]:
            print("A")
        if var[0][1]:
            print("B")
        if var[0][2]:
            print("X")
        if var[0][3]:
            print("Y")
        if var[0][4]:
            print("Start")
        if var[0][5]:
            print("Z")
        if var[0][6]:
            print("R")
        if var[0][7]:
            print("L")
        if var[0][8]:
            print("LS1")
        if var[0][9]:
            print("LS2")
        if var[1][0]:
            print("UP")
        if var[1][1]:
            print("DOWN")
        if var[1][2]:
            print("LEFT")
        if var[1][3]:
            print("RIGHT")
        if var[2][0]:
            print("C-UP")
        if var[2][1]:
            print("C-DOWN")
        if var[2][2]:
            print("C-LEFT")
        if var[2][3]:
            print("C-RIGHT")
        if var[3][0]:
            print("ModX")
        if var[3][1]:
            print("ModY")








