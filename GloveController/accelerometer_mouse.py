'''
Class which reads the values sent from the glove controller
and moves the mouse cursor.

If you're launching this code for the first time,
you'll need to set the Port of the controller.
To do it, GOTO the connect_device() method
and follow the instructions provided there.
'''

import serial
from matplotlib import pyplot as plt
import pyautogui
from GloveController import config


class AccelerometerMouse:
    '''
    This is the main method where all the magic happens.
    When called it will attempt to connect to the
    device on a designated port and after that
    it will read the data stream, interpret it and extract useful
    data which will be used to move the mouse cursor
    '''
    def start(self):
        '''Get the size of the screen'''
        screen_x, screen_y = pyautogui.size()

        '''Get the speed multiplier for X and Y axis'''
        mouse_speed_x = config.mouse_speed_x
        mouse_speed_y = config.mouse_speed_y

        '''Get the minimum value which will cause
        the mouse to move in either X or Y axis'''
        register_move_x_threshold = config.register_move_x_threshold
        register_move_y_threshold = config.register_move_y_threshold

        '''Get the label which is used
        to determine what value belongs to
        which parameter.
        It's determined in the micro-controller's code'''
        mouse_x_movement_label = config.mouse_x_movement_label
        mouse_y_movement_label = config.mouse_y_movement_label

        '''If the user chose to swap X and Y axis
        the solution will simply swap the labels which it uses
        to look for correct data'''
        if config.swap_xy:
            mouse_x_movement_label = config.mouse_y_movement_label
            mouse_y_movement_label = config.mouse_x_movement_label

        print('Mouse Is Running')

        '''Method which establishes a connection between
        the client and the server.
        In order to run this you'll need to the 
        Arduino Studio(or whichever other IDE you're using)
        and check the Port on which the controller runs.
        In Arduino Studio you can do it by Clicking Tools and then Port.'''
        def connect_device():
            '''Attempts to connect to the controller'''
            try:
                '''Replace COM3 with whichever port your
                controller runs on'''
                device = serial.Serial("COM3", 115200, timeout=1)
                return device
            except serial.SerialException as e:
                '''If an error occurs, the user will be asked to resolve it
                and then press enter.'''
                if 'Access is denied' in str(e):
                    input('Error, Device port is being used by a different program, '
                          'please turn it off and press enter')
                    device = connect_device()
                elif 'FileNotFoundError' in str(e):
                    input('Error, Device not found, it is most likely not connected. Please connect it and press enter')
                    device = connect_device()
                return device

        '''
        Method which moves the mouse as well as determine when it should move.
        Warning! It contains some legacy code, which upon removal caused issues.
        Don't touch them!
        '''
        def move_mouse(movement_x, movement_y):
            global screen_x
            global screen_y
            if abs(movement_x) >= register_move_x_threshold or abs(movement_y) >= register_move_y_threshold:
                print(f'movement_x: {movement_x} | movement_y: {movement_y}')

            if abs(movement_x) >= register_move_x_threshold or abs(movement_y) >= register_move_y_threshold:
                mouse_coord_x = movement_x * mouse_speed_x
                mouse_coord_y = movement_y * mouse_speed_y

                pyautogui.move(mouse_coord_x, mouse_coord_y)
                monitor_mouse_pos()
                # sleep(0.1)

        '''Clicks the Left mouse button'''
        def click_LMB():
            pyautogui.click(button='left')
            print('Clicked LMB')

        '''Clicks the Right mouse button'''
        def click_RMB():
            pyautogui.click(button='right')
            print('Clicked RMB')

        '''This method could be used to generate graphs of the retrieved data'''
        def monitor_x_y(movement_x, movement_y, counter, sample_size=300):
            x_arr.append(movement_x)
            y_arr.append(movement_y)
            if counter == sample_size:
                plt.plot(x_arr, color='blue')
                plt.plot(y_arr, color='green')
                plt.show()
            print(counter)
            return counter + 1

        '''Method which is used to monitor the current
        position of the cursor.'''
        def monitor_mouse_pos():
            x, y = pyautogui.position()
            print(f'x: {x} | y: {y}')

        '''x_arr and y_arr are used for plotting 
        the retrieved data'''
        x_arr = []
        y_arr = []

        sample_counter = 0

        '''The readings retrieved from the controller
        which will dictate how the mouse should behave.'''
        mouse_movement_x = 0
        mouse_movement_y = 0

        '''Mostly deprecated variables which serve no function.
        They were not removed as over the course of development
        the code has shown itself to be quite sensitive to 
        seemingly harmless changes.'''
        mouse_pos_x, mouse_pos_y = pyautogui.position()
        old_mouse_pos_x, old_mouse_pos_y = pyautogui.position()
        move_thresh = 3
        move_speed = 10

        '''Will invert the axis, if needed.
        By default the are inverted'''
        invert_x = -1 * config.invert_x
        invert_y = -1 * config.invert_y

        '''Connects to the mouse'''
        mouse = connect_device()

        '''Main loop'''
        while True:
            '''Attempts to read a line of the flushed data from the controller'''
            try:
                cc = str(mouse.readline())
            except UnboundLocalError as e:
                input('Error, device not found. Please, connect the device and press Enter')
                continue
            '''If successful some bloody magic will be used to 
            convert the data stream into usable data.
            That data is then split by ": " into 2 elements
            one of which is the label and the second one 
            is the data'''
            chunk = cc[2:][:-5].split(': ')
            if len(chunk) == 2:
                if chunk[0] == mouse_x_movement_label:
                    mouse_movement_y = float(chunk[1]) * invert_y
                if chunk[0] == mouse_y_movement_label:
                    mouse_movement_x = float(chunk[1]) * invert_x
                if chunk[0] == config.LMB_label:
                    if int(chunk[1]) == 1:
                        click_LMB()
                if chunk[0] == config.RMB_label:
                    if int(chunk[1]) == 1:
                        click_RMB()

            '''This calls the function which moves the mouse'''
            move_mouse(mouse_movement_x, mouse_movement_y)
