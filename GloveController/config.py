'''
This is a configuration file.

the accelerometer_mouse class reads from it
and the main menu takes user input to set
most of the parameters below.

Parameters are not saved between sessions,
because the config has be developed as a .py
file.
If saving parameters between sessions ever
becomes a priority, this file should be converted
into a JSON handler class
and the parameters should be stored in a JSON file.

I didn't do it, because it don't really care
about saving parameters between sessions :).
'''

'''
Sets the label which is used
to determine what value belongs to
which parameter.
It's determined in the micro-controller's code     
'''
mouse_x_movement_label = 'mouseMovementX'
mouse_y_movement_label = 'mouseMovementY'

LMB_label = 'LMB'
RMB_label = 'RMB'


'''
Sets the speed multiplier for X and Y axis
'''
mouse_speed_x = 15
mouse_speed_y = 15

'''
Sets the minimum value which will cause
the mouse to move in either X or Y axis
'''
register_move_x_threshold = 3
register_move_y_threshold = 3

'''
Sets whether or not X or Y axis 
should be inverted
'''
invert_x = 1
invert_y = 1

'''
Sets whether or not the X and Y axis
should be swapped
'''
swap_xy = False

'''
Starts the mouse
'''
start_mouse = False
