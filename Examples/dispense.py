from ModbusUtil import PGVA

s = PGVA()  # create a pgva using all the default settings

print(s.dispense(450, 10000))  # actuate the valve for 10 seconds with 450 mBar of pressure

s.finish()  # close the connection before finishing
