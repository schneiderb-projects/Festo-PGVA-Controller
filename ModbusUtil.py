from .pyModbusTCP.client import ModbusClient
from time import sleep

class Constants:
    HOLDING_REGISTERS_RANGE_BEGIN = 0x1000
    VALVE_ACTUATION_TIME_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 0
    VACUUM_THRESHOLD_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 1
    PRESSURE_THRESHOLD_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 2
    VEAB_SETPOINT_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 3
    DAC_MIN_450_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 4
    DAC_0_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 5
    DAC_PLUS_450_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 6
    ADC_MIN_450_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 7
    ADC_0_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 8
    ADC_PLUS_450_REGISTER = HOLDING_REGISTERS_RANGE_BEGIN + 9
    DAC_MIN_450_VAL = 155
    DAC_0_VAL = 1915
    DAC_PLUS_450_VAL = 3680
    ADC_MIN_450_VAL = 640
    ADC_0_VAL = 1871
    ADC_PLUS_450_VAL = 1964
    READ_OUTPUT_PRESSURE_REGISTER = 0x102
    READ_PRESSURE_TANK_REGISTER = 0x101
    READ_VACUUM_TANK_REGISTER = 0x100
    STATIC_IP = "192.168.10.102"
    NODE_ADDRESS = 0x10

class Register:
    HOLDING_REGISTER = 0
    INPUT_REGISTER = 1

    def __init__(self, register_address, register_type, modbus_client):
        """
            Constuctor for Register object
            :param register_address: register address (0 to 65535)
            :type register_address: int
            :param register_type: Type of register. Use Register class static variables
            :type register_type: int
            :param modbus_client: ModbusClient object
            :type modbus_client: ModbusClient
        """
        self.register_address = register_address
        self.__check_type(register_type) # check if the register type is valid
        self.register_type = register_type
        self.modbus_client = modbus_client

    def write(self, value):
        """
            Writes to a single register
            :param value: register value to write
            :type value: int
            :returns: True if write ok or None if fail
            :rtype: bool or None
        """
        if self.register_type == Register.HOLDING_REGISTER or self.register_type == Register.INPUT_REGISTER:
            return self.modbus_client.write_single_register(self.register_address, value)

        else:
            raise Exception("invalid register type. Only use Register class static variables (i.e. Register.foo)")

    def read(self):
        if self.register_type == Register.INPUT_REGISTER:
            return self.modbus_client.read_input_registers(self.register_address)
        elif self.register_type == Register.HOLDING_REGISTER:
            return self.modbus_client.read_holding_registers(self.register_address)

    def print(self):
        """
            read register and print the value to the console
            :returns: Returns the register value or None if read fails
            :rtype: int or None
        """
        out = self.read()
        print("register ", hex(self.register_address), ": val = ", out)
        return out

    def __check_type(self, type):
        if type < 0 or type > Register.INPUT_REGISTER:
            raise Exception("invalid register type. Use Register class static variables (i.e. Register.foo)")
            return False
        return True


class PGVA:
    def __init__(self, ip_address=Constants.STATIC_IP, port=8502,
                 node_address=Constants.NODE_ADDRESS,
                 valve_register=Constants.VALVE_ACTUATION_TIME_REGISTER,
                 pressure_register=Constants.VEAB_SETPOINT_REGISTER,
                 pressure_actual_register=Constants.READ_OUTPUT_PRESSURE_REGISTER,
                 DAC_Min_Register=Constants.DAC_MIN_450_REGISTER, DAC_Zero_Register=Constants.DAC_0_REGISTER,
                 DAC_Max_Register=Constants.DAC_PLUS_450_REGISTER, ADC_Min_Register=Constants.ADC_MIN_450_REGISTER,
                 ADC_Zero_Register=Constants.ADC_0_REGISTER, ADC_Max_Register=Constants.ADC_PLUS_450_REGISTER,
                 DAC_Min_Val=Constants.DAC_MIN_450_VAL, DAC_0_Val=Constants.DAC_0_VAL,
                 DAC_Max_Val=Constants.DAC_PLUS_450_VAL, ADC_Min_Val=Constants.ADC_MIN_450_VAL,
                 ADC_0_Val=Constants.ADC_0_VAL, ADC_Max_Val=Constants.ADC_PLUS_450_VAL,
                 pressure_tank_actual=Constants.READ_PRESSURE_TANK_REGISTER,
                 vacuum_tank_actual=Constants.READ_VACUUM_TANK_REGISTER):
        """
            Constuctor for PGVA
            :param ip_address: ip_address of the pressure box
            :type ip_address: str
            :param port: port number for Modbus connection
            :type port: int
            :param node_address: node address of the pressure box
            :type node_address: int
            :param valve_register: register to actuate the valve
            :type modbus_client: int
            :param pressure_register: register to change the pressure
            :type pressure_register: int
            :param DAC_Min_Register: calibrate DAC value for -450 mBar
            :type DAC_Min_Register: int
            :param DAC_Zero_Register: calibrate DAC value for 0 mBar
            :type DAC_Zero_Register: int
            :param ADC_Min_Register: calibrate ADC value for -450 mBar
            :type ADC_Min_Register: int
            :param ADC_Zero_Register: calibrate ADC value for 0 mBar
            :type ADC_Zero_Register: int
            :param ADC_Max_Register: calibrate ADC value for 450 mBar
            :type ADC_Max_Register: int
            :param DAC_Min_Register: calibrate DAC value for -450 mBar
            :type DAC_Min_Register: int
            :param DAC_Zero_Register: calibrate DAC value for 0 mBar
            :type DAC_Zero_Register: int
            :param ADC_Min_Register: calibrate ADC value for -450 mBar
            :type ADC_Min_Register: int
            :param ADC_Zero_Register: calibrate ADC value for 0 mBar
            :type ADC_Zero_Register: int
            :param ADC_Max_Register: calibrate ADC value for 450 mBar
            :type ADC_Max_Register: int
        """
        self.lastPressure = 0

        self.client = ModbusClient(host=ip_address, port=port, auto_open=True,
                         unit_id=node_address, auto_close=False, timeout=5)

        self.client.open()

        if self.client.is_open():
            print("TCP connection successful")
        else:
            print("TCP connection unsuccessful")
            raise RuntimeError("Unable to Connect to PGVA Box ")

        self.valve = Register(valve_register, Register.HOLDING_REGISTER, self.client)
        self.pressure = Register(pressure_register, Register.HOLDING_REGISTER, self.client)
        self.pressure_output_actual = Register(pressure_actual_register, Register.INPUT_REGISTER, self.client)
        self.pressure_tank_actual = Register(pressure_tank_actual, Register.INPUT_REGISTER, self.client)
        self.vacuum_tank_actual = Register(vacuum_tank_actual, Register.INPUT_REGISTER, self.client)
        self.has_liquid = False
        self._calibrate(Register(DAC_Min_Register, Register.HOLDING_REGISTER, self.client),
                        Register(DAC_Zero_Register, Register.HOLDING_REGISTER, self.client),
                        Register(DAC_Max_Register, Register.HOLDING_REGISTER, self.client),
                        Register(ADC_Min_Register, Register.HOLDING_REGISTER, self.client),
                        Register(ADC_Zero_Register, Register.HOLDING_REGISTER, self.client),
                        Register(ADC_Max_Register, Register.HOLDING_REGISTER, self.client),
                        DAC_Min_Val, DAC_0_Val, DAC_Max_Val, ADC_Min_Val,
                        ADC_0_Val, ADC_Max_Val)

    def _calibrate(self, DAC_Min_Register, DAC_Zero_Register,
                   DAC_MaxVal_Register, ADC_MinVal_Register,
                   ADC_ZeroVal_Register, ADC_MaxVal_Register,
                   DAC_Min_Val, DAC_0_Val, DAC_Max_Val,
                   ADC_Min_Val, ADC_0_Val, ADC_Max_Val):
        print("Calibrating DAC_MinVal:", DAC_Min_Register.write(DAC_Min_Val))
        print("Calibrating DAC_ZeroVal: ", DAC_Zero_Register.write(DAC_0_Val))
        print("Calibrating DAC_MaxVal: ", DAC_MaxVal_Register.write(DAC_Max_Val))
        print("Calibrating ADC_MinVal:", ADC_MinVal_Register.write(ADC_Min_Val))
        print("Calibrating ADC_ZeroVal:", ADC_ZeroVal_Register.write(ADC_0_Val))
        print("Calibrating ADC_MaxVal:", ADC_MaxVal_Register.write(ADC_Max_Val))

        '''print("DAC_MinVal:", DAC_Min_Register.read())
        print("DAC_ZeroVal:", DAC_Zero_Register.read())
        print("DAC_MaxVal:", DAC_MaxVal_Register.read())
        print("ADC_MinVal:", ADC_MinVal_Register.read())
        print("ADC_ZeroVal:", ADC_ZeroVal_Register.read())
        print("ADC_MaxVal:", ADC_MaxVal_Register.read())'''

    def open_valve(self, time):
        """
            open valve for a given time in ms
            :param time: time the valve is opened in ms
            :type time: int
            :return:True if the valve is opened successfully or None if unsuccessful
        """
        if self.client.is_open():
            out = self.valve.write(time)
            sleep((time/1000.0) + 2.5/1000 + 1)
            return out
        return None

    def set_pressure(self, pressure, delay=True):
        """
            set pressure to given pressure
            :param pressure: pressure in mbar
            :type pressure: int
            :param delay: determine if the program should wait for the pressure to change
            :type pressure: boolean
            :return:True if the pressure is set successfully or None if unsuccessful
        """

        self.lastPressure = pressure

        pressure = (int)(pressure * 4.096 + 2047)

        if self.read_pressure()[0] == pressure:
            return True

        out = self.pressure.write(pressure)
        if delay:
            sleep(1)
        return out

    def aspirate(self, pressure, time, ignore_protections = False):
        """
        aspirate fluid using a given pressure for a given time
        :param pressure: pressure in mbar
        :type pressure: int
        :param time: time the valve is opened in ms
        :type time: int
        :return True if the aspirate is successfully, None if unsuccessful or pipette already has liquid, and False if TCP connection is not open
        """
        '''if ignore_protections:
            self.has_liquid = False

        if self.has_liquid:
            raise Exception("Pipette already has liquid aspirated. Dispense liquid first or set ignore_protections=True")'''

        if self.client.is_open():
            print("TCP is connected")
            out_p = self.set_pressure(-1 * pressure)
            out_v = self.open_valve(time)

            if out_v and out_p:
                self.has_liquid = True
                return True
            else:
                self.has_liquid = False
                return None
        print("TCP connection failure")
        return False


    def finish(self):
        """
        always call this at the end of your protocol
        """
        self.client.close()

    def dispense(self, pressure, time):
        """
        dispense fluid using a given pressure for a given time
        :param pressure: negative pressure in mbar (use positive number)
        :type pressure: int
        :param time: time the valve is opened in ms
        :type time: int
        :return True if the aspirate is successfully, None if unsuccessful, and False if TCP connection is not open
        """
        #self.has_liquid = False
        out = self.aspirate(-1 * pressure, time)
        '''if out:
            self.has_liquid = False
        else:
            self.has_liquid = True'''

        return out

    def read_pressure(self):
        out = self.pressure_output_actual.read()
        #print("pressure: " + str(out))
        #return [self.lastPressure]
        return out

    def read_vacuum_tank(self):
        out = self.vacuum_tank_actual.read()
        # print("pressure: " + str(out))
        # return [self.lastPressure]
        return out

    def read_pressure_tank(self):
        out = self.pressure_tank_actual.read()
        # print("pressure: " + str(out))
        # return [self.lastPressure]
        return out

    def read_current_setpoint(self):
        out = self.pressure.read()
        # print("pressure: " + str(out))
        # return [self.lastPressure]
        return out

    def is_open(self):
        self.client.is_open()

    def open(self):
        self.client.open()
