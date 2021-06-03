'''
Main file.
Due to technical limitations of the tkinter library,
Mouse codebase had to be wrapped inside the
GUI settings menu
Rather than developing them as 2 separate classes
Initializing the in the main file.
This file is mostly responsible for creating a settings menu where
Certain parameters of the mouse can be configured
As well as serving as a starting point
From which the mouse can be launched
'''
from tkinter import *
from GloveController import accelerometer_mouse, config

# Init the GUI class and set the dimensions
# of the window
gui = Tk(className='Mouse Config')
gui.geometry("400x200")

# ========================================
# Read the preset values to set the
# starting values of the sliders
mouse_speed_x = config.mouse_speed_x
mouse_speed_y = config.mouse_speed_y

register_move_x_threshold = config.register_move_x_threshold
register_move_y_threshold = config.register_move_y_threshold
# ========================================


# ========================================
# Init the IntVar() class from the tkinter
# library
invert_x = IntVar()
invert_y = IntVar()

swap_xy = IntVar()
# ========================================

# Used to determine whether
# the mouse should be turned on
mouse_state = 0


# Sets the invert_x var in the config
# which dictates whether the X axis
# Should be inverted
def set_invert_x():
    # tkinter checkboxes return either 1 or 0
    # rather than 1 or -1
    # hence this conversion
    if invert_x.get() == 1:
        config.invert_x = -1
    else:
        config.invert_x = 1


# Sets the invert_y var in the config
# which dictates whether the Y axis
# Should be inverted
def set_invert_y():
    # tkinter checkboxes return either 1 or 0
    # rather than 1 or -1
    # hence this conversion
    if invert_y.get() == 1:
        config.invert_y = -1
    else:
        config.invert_y = 1


# Sets the swap_xy var in the config
# which dictates whether the X and Y
# axis should be swapped
def set_swap_xy():
    # tkinter checkboxes return either 1 or 0
    # rather than True or False
    # hence this conversion
    if swap_xy.get() == 1:
        config.swap_xy = True
    else:
        config.swap_xy = False


# Sets the mouse_speed_x var in the config
# which stores the speed multiplier
# of the X axis
def set_mouse_speed_x():
    config.mouse_speed_x = widget_mouse_speed_x.get()


# Sets the mouse_speed_y var in the config
# which stores the speed multiplier
# of the Y axis
def set_mouse_speed_y():
    config.mouse_speed_y = widget_mouse_speed_y.get()


# Sets the register_move_x_threshold var in the config
# which stores minimum value which can cause
# the mouse to move on the X axis
def set_register_move_x_threshold():
    config.register_move_x_threshold = widget_register_move_x_threshold.get()


# Sets the register_move_y_threshold var in the config
# which stores minimum value which can cause
# the mouse to move on the Y axis
def set_register_move_y_threshold():
    config.register_move_y_threshold = widget_register_move_y_threshold.get()


# Starts the mouse
def set_mouse_state():
    config.start_mouse = mouse_state


# Contains some legacy code!
# Controls some of the properties of the
# start button
# when clicked calls set_mouse_state() method
# which changes the state of the start_mouse var
# then creates an instance of the accelerometer_mouse
# class as mouse and runs the start() method
# which launches the device
def manage_button_change_mouse_state():
    global mouse_state

    if mouse_state == 0:
        mouse_state = 1
        button_change_mouse_state['text'] = 'Stop'
        gui.destroy()

        mouse = accelerometer_mouse.AccelerometerMouse()
        mouse.start()

    elif mouse_state == 1:
        mouse_state = 0
        button_change_mouse_state['text'] = 'Start'
    set_mouse_state()


# ========================================
# Create all Labels in the menu
label_mouse_speed_x = Label(text="X axis sensitivity")
label_mouse_speed_y = Label(text="Y axis sensitivity")
label_register_move_x_threshold = Label(text="X Threshold")
label_register_move_y_threshold = Label(text="Y Threshold")
# ========================================

# ========================================
# Create all widgets in the menu i.e. sliders
# and set their starting values
widget_mouse_speed_x = Scale(gui, from_=1, to=30)
widget_mouse_speed_x.set(mouse_speed_x)
widget_mouse_speed_y = Scale(gui, from_=1, to=30)
widget_mouse_speed_y.set(mouse_speed_y)

widget_register_move_x_threshold = Scale(gui, from_=0, to=15)
widget_register_move_x_threshold.set(register_move_x_threshold)
widget_register_move_y_threshold = Scale(gui, from_=0, to=15)
widget_register_move_y_threshold.set(register_move_y_threshold)
# ========================================

# ========================================
# Create all checkboxes in the menu
checkbox_invert_x = Checkbutton(gui, text='Invert X', command=set_invert_x, variable=invert_x)
checkbox_invert_y = Checkbutton(gui, text='Invert Y', command=set_invert_y, variable=invert_y)
checkbox_swap_xy = Checkbutton(gui, text='Swap X and Y', command=set_swap_xy, variable=swap_xy)
# ========================================

# ========================================
# Create all buttons in the menu
button_mouse_speed_x = Button(gui, text="Set", command=set_mouse_speed_x)
button_mouse_speed_y = Button(gui, text="Set", command=set_mouse_speed_y)
button_register_move_x_threshold = Button(gui, text="Set", command=set_register_move_x_threshold)
button_register_move_y_threshold = Button(gui, text="Set", command=set_register_move_y_threshold)
button_change_mouse_state = Button(gui, text='Start', command=manage_button_change_mouse_state)
# ========================================

# ========================================
# Organize all elements of the menu
# using tkinter's grid() method
label_mouse_speed_x.grid(column=0, row=0)
label_mouse_speed_y.grid(column=1, row=0)
label_register_move_x_threshold.grid(column=2, row=0)
label_register_move_y_threshold.grid(column=3, row=0)

checkbox_invert_x.grid(column=0, row=3)
checkbox_invert_y.grid(column=1, row=3)
checkbox_swap_xy.grid(column=2, row=3)

widget_mouse_speed_x.grid(column=0, row=1)
widget_mouse_speed_y.grid(column=1, row=1)
widget_register_move_x_threshold.grid(column=2, row=1)
widget_register_move_y_threshold.grid(column=3, row=1)

button_mouse_speed_x.grid(column=0, row=2)
button_mouse_speed_y.grid(column=1, row=2)
button_register_move_x_threshold.grid(column=2, row=2)
button_register_move_y_threshold.grid(column=3, row=2)
button_change_mouse_state.grid(column=3, row=3)
# ========================================

# Start the menu loop
mainloop()
