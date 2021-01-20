from opentrons import containers, instruments, robot
import sys
sys.path.insert(1, '/Users/brettschneider/PycharmProjects/testProtocol/')
from ModbusUtil import Register
from pyModbusTCP.client import *

c = ModbusClient(host="192.168.10.102", port=8502, auto_open=True, unit_id=0x10, auto_close=False,timeout=10)
c.open()
r = Register(0x1000, Register.HOLDING_REGISTER, c)

plate = containers.load('96-flat', 'B1', 'my-plate')
tiprack = containers.load('tiprack-200ul', 'A1', 'my-rack')

pipette = instruments.Pipette(axis='b', max_volume=200, name='my-pipette')

#chdir("/Users/brettschneider/PycharmProjects/testProtocol")

robot.comment(getcwd())

for i in range(96):
    robot.move_to(plate[i])
    out = r.write(100)
    if out == None:
        raise Exception("None")
