from Gantry.Gantry import Gantry
from Labware.Plates.Plate import Plate96
from Motors.CMMO.CMMO import CMMO

# top left bottom: [188, 93.8, 20]
# top right bottom: [188, 156, 20]
# bottom left bottom: [88.5, 93.8, 20]

'''
    Uses a 3 axis CMMO gantry to fill a plate
    
    This just does the moments, it doesn't actually aspirate or dispense any liquid
'''

x_CMMO_ip_address = "172.21.48.20"  # ip address of the CMMO controlling the x axis
y_CMMO_ip_address = "172.21.48.22"  # ip address of the CMMO controlling the y axis
z_CMMO_ip_address = "172.21.48.24"  # ip address of the CMMO controlling the z axis

all_axes = [x_CMMO_ip_address, y_CMMO_ip_address, z_CMMO_ip_address]  # add all ip addresses into a list
gantry = Gantry(all_axes, CMMO)  # Gantry(list of CMMO ip addresses)
gantry.enable()  # Turn on the motors. Must enable the gantry in order to move or home.

gantry.setVelocities([116, 92, 160])

gantry.home(verboseGantry=True, motors=[2])  # Homes z axes of the gantry
gantry.home(verboseGantry=True, motors=[1, 0])  # Homes x y axes of the gantry

plate = Plate96([188, 93.8], [188, 156], [88.5, 93.8], 20, 11)
# Plate96(3 sets of x, y coordinates for 3 corners of the plate,
# z coordinate for the bottom of the plate z coordinate for the
# top of the plate)

for row in range(12):
    for column in range(8):
        [x, y] = plate.getWell(row, column)
        gantry.moveTo([None, None, plate.getTop()])
        gantry.moveTo([x, y, None])
        gantry.moveTo([None, None, plate.getBottom()])
        #gantry.moveTo([None, None, None, None, plate.getTop()])
