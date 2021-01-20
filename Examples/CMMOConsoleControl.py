from Gantry.Gantry import Gantry
import Motors.CMMO.CMMO as CMMO

'''
    Program to use the Gantry library in order to control a three axis CMMO gantry with X, Y, and Z axis.
    
    Additional axes can be added easily by adding addition IP address when initializing
'''

x_CMMO_ip_address = "172.21.48.20"  # ip address of the CMMO controlling the x axis
y_CMMO_ip_address = "172.21.48.22"  # ip address of the CMMO controlling the y axis
z_CMMO_ip_address = "172.21.48.24"  # ip address of the CMMO controlling the z axis

all_axes = [x_CMMO_ip_address, y_CMMO_ip_address, z_CMMO_ip_address]  # add all ip addresses into a list

gantry = Gantry(all_axes, CMMO)  # Gantry(list of CMMO ip addresses)
gantry.enable()  # Turn on the motors. Must enable the gantry in order to move or home.
gantry.home()  # Homes all axis of the gantry

gantry.setVelocities([116, 92, 160])  # set the velocities. Use FCT to determine acceptable velocities for your motor.


def checkDigit(digit_str):  # check if a string can be converted to an int
    try:
        int(digit_str)
    except:
        return False

    return True


while True:  # Infinite loop
    inp = input("Input coordinate (x y z) or H (home) or D (Disable) or E (Enable): ")  # get user input
    split_inp = inp.split(" ")
    if 'H' in inp:
        gantry.home(verboseGantry=True)  # Home gantry
    elif 'D' in inp:
        gantry.disable(verboseGantry=True)  # disable all motors of gantry
                                            # use gantry.disable(motors=[list of indexs]) to disable specific motors
    elif 'E' in inp:
        gantry.enable(verboseGantry=True)  # Disconnect from CMMO
                                           # use gantry.enable(motors=[list of indexs]) to disable specific motors
    elif len(split_inp) > 0:  # check user input
        coordinate = []
        for coord in split_inp:
            coordinate.append(float(coord))  # add the user input into a list
        gantry.moveTo(coordinate, verboseGantry=True)  # moveTo(list of locations)
    else:
        print("invalid input, try again")
