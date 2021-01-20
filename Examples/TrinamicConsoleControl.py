from Gantry.Gantry import Gantry
from Gantry.LowPayloadGantry import initialPositions, setupFunction, homeVelocity
import Motors.Trinamic.TrinamicMotor as TrinamicMotor

'''
    program to use the Gantry library in order to control a 5 axis gantry with X, 2 Y's, and 2 Z's axes.
'''

all_axes = list(range(0, 5))  # add all motor ID's into a list

gantry = Gantry(all_axes, TrinamicMotor, setupFunction=setupFunction)  # Gantry(list of CMMO ip addresses)
gantry.connect()
gantry.enable()  # Turn on the motors. Must enable the gantry in order to move or home.
#gantry.home(verboseGantry=True)  # Homes all axis of the gantry

#print("homed")


def checkDigit(digit_str):  # check if a string can be converted to an int
    try:
        int(digit_str)
    except:
        return False

    return True

gantry.setVelocities(homeVelocity)

while True:  # Infinite loop
    inp = input("Input coordinate (Y1 Z1 X Y2 Z2) or H (home) or D (Disable) or E (Enable) or I (Initial Positions) or "
                "C (Center): ")  # get user input
    split_inp = inp.split(" ")
    if 'H' in inp:
        gantry.home()  # Home gantry
        print(gantry.getCurrentPositions())

    elif 'I' in inp:
        gantry.moveTo(initialPositions, verboseGantry=True)  # moveTo(list of locations)
        print(gantry.getCurrentPositions())

    elif 'C' in inp:
        gantry.moveTo([3000 * 6, -8000/2, -28500/2, -3000 * 6, -8000/2], verboseGantry=True)  # moveTo(list of locations)
        print(gantry.getCurrentPositions())

    elif 'D' in inp:
        gantry.disable(verboseGantry=True)  # disable all motors of gantry
        # use gantry.disable(motors=[list of indexs]) to disable specific motors
    elif 'E' in inp:
        gantry.enable(verboseGantry=True)  # Disconnect from CMMO
        # use gantry.enable(motors=[list of indexs]) to disable specific motors

    elif 'G' in inp:
        gantry.moveRelative([0, 0, 0, 0, -300], verboseGantry=True)
        print(gantry.getCurrentPositions())

    elif 'A' in inp:
        gantry.moveRelative([0, 0, 0, 0, 300], verboseGantry=True)
        print(gantry.getCurrentPositions())

    elif 'R' in inp:
        gantry.moveRelative([0, 0, 0, 300, 0], verboseGantry=True)
        print(gantry.getCurrentPositions())

    elif 'L' in inp:
        gantry.moveRelative([0, 0, 0, -300, 0], verboseGantry=True)
        print(gantry.getCurrentPositions())

    elif 'F' in inp:
        gantry.moveRelative([0, 0, 300, 0, 0], verboseGantry=True)
        print(gantry.getCurrentPositions())

    elif 'B' in inp:
        gantry.moveRelative([0, 0, -300, 0, 0], verboseGantry=True)
        print(gantry.getCurrentPositions())

    elif len(split_inp) > 0:  # check user input
        coordinate = []
        try:
            for coord in split_inp:
                coordinate.append(int(coord))  # add the user input into a list
            gantry.moveTo(coordinate, verboseGantry=True)  # moveTo(list of locations)
            print(gantry.getCurrentPositions())
        except:
            print("invalid input, try again")

    else:
        print("invalid input, try again")
