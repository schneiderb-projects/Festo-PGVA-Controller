from Labware.Pipettes.PGVA.ModbusUtil import PGVA

'''
    Example of how to use PGVA class to aspirate and dispense by setting the pressure
    then using a open loop pipette
'''

pgva = PGVA()

pgva.aspirate(100, 100)  # set vacuum to 100 mbar then actuate valve for 100 ms
pgva.dispense(100, 100)  # set pressure to 100 mbar then actuate valve for 100 ms

pgva.finish()
