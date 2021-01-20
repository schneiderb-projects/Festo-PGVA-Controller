from ModbusUtil import PGVA

volume = 200  # volume in mL
pressure = 100  # pressure in mBar
time = (38.028*volume - 543.49) * (pressure**-0.565)  # very rough equation to calculate actuation time given a pressure
                                                      # and desired volume in order to ASPIRATE that volume

print("time: " + str(time))

s = PGVA()  # initialize PGVA using default settings

s.dispense(100, 100)  # actuate the valve for 100 ms at 100 mBar pressure

s.aspirate(pressure, time)  # actuate the valve for the desired time and pressure

s.finish()  # close the connection
