import canopen
import time



class Motor:


    cw_switch_on = b'\x0F\x00'
    cw_switch_off = b'\x06\x00\x00'
    cw_stop_homing = b'\x0F\x00'
    cw_start_homing = b'\x1F\x00'
    cw_start_positioning = b'\x1F\x00'
    cw_rel_start_positioning=b'\x5F\x00'
    cw_prep_nxt_position=b'\x4F\x00'
    sw_commutation_found=0xc037
    sw_reference_found = 0xd437
    sw_homing_finished_successfully=0xc437
    sw_target_position_acknowledged= 0xd037
    sw_position_reached=0xc037
    sw_target_reached = 0xc437
    sw_turned_off_1 ="0xc031"
    sw_turned_off_2 = "0xd031"
    cw_set_homing_19=b'\x13\x00'
    cw_set_homing_34=b'\x22\x00'

    def __init__(self,node: canopen.Node) :
        self.node=node

    def init(self):

        """Switch-on servo amplifier"""

        self.node.sdo.download(0x6040, 0,self.cw_switch_on)
        #node.sdo.download(0x6060, 0, b'\x06\x00')
        #node.sdo.download(0x6040, 0, b'\x1F\x00')
        #time.sleep(1)
        #node.sdo.download(0x6060, 0, b'\x01\x00')
        #node.sdo.download(0x6081, 0, b'\x40\x42\x0F\x00')
        #node.sdo.download(0x607A, 0, b'\xA0\x86\x01\x00')
        #node.sdo.download(0x6040, 0, b'\x1F\x00')



    def halt(self):
        """Switch-on servo amplifier"""
        self.node.sdo.download(0x6040, 0,self.cw_switch_off)
    @staticmethod
    def int_to_byte(an_int):
      a_bytes_little = an_int.to_bytes(4, 'little')
      return an_int.to_bytes(4, 'little')

    @property
    def operating_mode(self):
        op_mode = self.node.sdo[0x6061].raw

        return op_mode

    @operating_mode.setter
    def operating_mode(self, val):
        """
        Change to operating mode
            1: Positioning
            3: Velocity mode
            4: Profile torque mode for direct current setpoint setting
            6: Homing
            7: Interpolated mode with command (ECOVARIO®, ECOMODUL, ECOMPACT)
            8: Cyclic synchronous position mode (not E100/E400, ECOMODUL)
            9: Cyclic synchronous velocity mode
        """
        if val not in [1, 3, 4, 6, 7, 8, 9]:
            raise ValueError(f'Invalid mode {val}')
        self.node.sdo.download(0x6060, 0,self.int_to_byte(val))


    @property
    def status(self):
        """Read status word"""
        answer = self.node.sdo[0x6041].raw
        hex_answer=hex(answer)
        return hex_answer

    def stop_homing(self):
        """Reset control word"""
        self.node.sdo.download(0x6040, 0,self.cw_stop_homing )
        #print('Stop homing')

    def start_homing(self):
        """Start homing"""
        self.node.sdo.download(0x6040, 0,self.cw_start_homing)
        #print('start homing')
    def start_positioning(self):
        """Start positioning"""

        self.node.sdo.download(0x6040, 0, self.cw_start_positioning)
    def rel_start_positioning(self):
        """Start positioning"""

        self.node.sdo.download(0x6040, 0, self.cw_rel_start_positioning)


    def prep_nxt_position(self):
        """Start positioning"""

        self.node.sdo.download(0x6040, 0, self.cw_prep_nxt_position)

    @property
    def acceleration(self):
        """:return: Actual motor velocity"""
        pass

    @acceleration.setter
    def acceleration(self, val: float):
        """Set the motor velocity in Turns/s"""
        factor = 2500
        data = self.int_to_byte(round(val * factor))

        self.node.sdo.download(0x6083, 0, data)

    @property
    def deceleration(self):
        """:return: Actual motor deceleration"""
        pass

    @deceleration.setter
    def deceleration(self, val: float):
        """Set the motor velocity in Turns/s"""
        factor = 2500
        data = self.int_to_byte(round(val * factor))

        self.node.sdo.download(0x6084, 0, data)

    @property
    def target_velocity(self):
        return

    @target_velocity.setter
    def target_velocity(self, val: float):
        """Set the motor velocity in Turns/s"""
        factor = 2560000
        data = self.int_to_byte(round(val * factor))

        self.node.sdo.download(0x60FF, 0, data)
    @property
    def velocity(self):
        """:return: Actual motor velocity"""
        factor=int(40000*64)
        actual_speed_Dec = self.node.sdo[0x606C]
        #print(actual_speed_Dec.phys/factor)
        return actual_speed_Dec.phys/(factor)

    @velocity.setter
    def velocity(self, val: float):
        """Set the motor velocity in Turns/s"""
        factor = 2560000
        data = self.int_to_byte(round(val * factor))

        self.node.sdo.download(0x6081, 0, data)

    @property
    def turns(self):
        """:return: The number of evolutions of the motor since the last reset"""
        factor=40000
        actual_position_Dec = self.node.sdo[0x6063]
        #print(actual_position_Dec.phys / 40000 )
        return (actual_position_Dec.phys / factor)


    @turns.setter
    def turns(self, val:float):
        """Set the number of turns that shall be performed"""
        factor = 40000
        data1 = self.int_to_byte(round(val * factor))
        self.node.sdo.download(0x607A, 0, data1)

    def check_statusword(self, data, timeout=5.0):
        data1 = hex(data)
        if data1 != self.status:
            raise ValueError(f'Invalid status word {self.status}')
      #  timer = 0
       # ret = None

       # while timer < timeout:
         #   ret = self.status

         #   if ret != data1:
          #      time.sleep(0.1)
           #     timer += 0.1
           # else:
               # break
        #return ret
    def timeout_statusword(self, data, timeout=30.0):
        data1 = hex(data)
        timer = 0
        ret = None

        while timer < timeout:
            ret = self.status

            if ret != data1:
                time.sleep(0.1)
                timer += 0.1
            else:
                break
        return ret

    def run_n_turns(self, **kwargs):
        """
        Initializes the motor, sets the velocity and turns a defined number of evolutions
        :param kwargs:
            turns: Number of total evolutions
            velocity: Velocity of the motor in turns/s
        """
        self.init()
        self.operating_mode = 6
        self.start_homing()
        time.sleep(0.2)
        self.stop_homing()
        self.operating_mode = 1
        self.velocity = kwargs.get('velocity', 5)
        self.turns = kwargs.get('turns', 1)
        self.start_positioning()
        #self.shutdown()
        #self.halt()

    def Homing(self):
        """
        Homing for servo axis, initial situation after power-on

        """

        self.init()
        self.operating_mode = 6
        self.init()
        self.node.sdo.download(0x6098, 0, self.cw_set_homing_34)
        time.sleep(0.2)

        self.start_homing()

        #self.check_statusword(self.sw_reference_found)

        self.stop_homing()

        #self.check_statusword(self.sw_homing_finished_successfully)
        #self.start()

    def relative_positioning(self, **kwargs):
        """
        Positioning mode relative (1) after homing for servo axis, Status: control word=0x000F,
        status word=0xC437
        :param kwargs:
            turns: Number of total evolutions
            velocity: Velocity of the motor in turns/s
        """
        self.operating_mode = 1
        self.velocity = kwargs.get('velocity', 5)
        self.turns = kwargs.get('turns', 1)
        #self.acceleration = kwargs.get('acceleration', 1)
        self.rel_start_positioning()
        #print(m.status)
        ##self.check_statusword(self.sw_target_position_acknowledged)
        #self.timeout_statusword(self.sw_target_position_acknowledged)
        #print(m.status)

        self.prep_nxt_position()

        #print(m.status)
        ##self.check_statusword(self.sw_position_reached)
        #self.timeout_statusword(self.sw_position_reached)
        #print(m.status)
        #self.check_statusword(self.sw_target_reached)
        #self.timeout_statusword(self.sw_target_reached)
        #print(m.status)



    def absolute_positioning(self, **kwargs):
        """
        Positioning mode absolute (1) after homing for servo axis, Status: control word=0x000F,
        status word=0xC437
        :param kwargs:
            turns: Number of total evolutions
            velocity: Velocity of the motor in turns/s
        """
        self.operating_mode = 1
        self.velocity = kwargs.get('velocity', 5)
        self.turns = kwargs.get('turns', 1)
        self.start_positioning()
        # print(m.status)
        ##self.check_statusword(self.sw_target_position_acknowledged)
        #self.timeout_statusword(self.sw_target_position_acknowledged)
        self.init()
        # print(m.status)
        ##self.check_statusword(self.sw_commutation_found)
        # print(m.status)
        #self.timeout_statusword(self.sw_commutation_found)
        # print(m.status)
        #self.timeout_statusword(self.sw_target_reached)
        #print(m.status)
    def stop_absolute_positioning(self, **kwargs):
        """
        Positioning mode absolute (1) after homing for servo axis, Status: control word=0x000F,
        status word=0xC437
        :param kwargs:
            turns: Number of total evolutions
            velocity: Velocity of the motor in turns/s
        """
        self.operating_mode = 1
        self.velocity = 0
        self.turns = kwargs.get('turns', 1)
        self.start_positioning()

    def inquire_statusword_bool(self):
         sw_hex = self.node.sdo[0x6041].raw
         sw_bool = [bool(int(c)) for c in f"{sw_hex:016b}"]
         #print(y[0])
         #print(y)
         #print('Reference found is {0} , Commutation found is {1}'.format(y[0], y[1]))
         #print(' Reference error is {0} , Reference found is {1}'.format(y[2], y[3]))
         #print(' Internal limit active is {0} , Target reached is {1}'.format(y[4], y[5]))
         #print(' Reserved is {0} , Manufacturer specific  is {1}'.format(y[6], y[7]))
         #print(' Warning  is {0} , Switch on Disable is {1}'.format(y[8], y[9]))
         #print(' Quick Stop  is {0} , Voltage Enabled  is {1}'.format(y[10], y[11]))
         #print(' Fault is {0} , Operation Enable  is {1}'.format(y[12], y[13]))
         #print(' Switched on is {0} , Ready to switch on  is {1}'.format(y[14], y[15]))
         return sw_bool

    def velocity_mode(self,**kwargs):
        self.operating_mode = 3
        self.target_velocity=0
        self.init()
        self.target_velocity = kwargs.get('target_velocity', 5)

    def stop_velocity_mode(self):

        self.target_velocity = 0
    @property
    def inquire_DIN6(self):
        """return digital input value """
        actual_value = self.node.sdo[0x2122]
        #actual_value = self.node.sdo.upload(0x2122, 0)
        return actual_value.phys
    #b'\x02'
    def home_to_switch(self):
        """return digital input value """
        self.init()

        self.operating_mode=6
        self.node.sdo.download(0x6098, 0, self.cw_set_homing_19)#set Homing method
        self.node.sdo.download(0x6099, 1, b'\x40\x42\x0F')#set the  speed of homing 0.4 U/S
        #self.node.sdo.download(0x607C, 0, b'\x00\x00\x00')
        self.start_homing()
        #self.stop_homing()
        time.sleep(2)
        # self.stop_homing()
        #äself.init()
        self.absolute_positioning(turns=0.61,velocity=1)#set the offest to almost 180 Degree
        time.sleep(1)
        #print(self.status)
        # if self.status=="0xc437":
        #     self.Homing()
            

        # self.init()
        # self.operating_mode = 6
        # self.node.sdo.download(0x6098, 0, self.cw_set_homing_34)
        # self.start_homing()
        # time.sleep(2)
        # self.stop_homing()





    # def test(self):
    #        # x=self.node.tpdo.read()
    #        # print(x)
    #        factor = 40000
    #        actual_position_Dec = self.node.pdo[0x6063]
    #        print(actual_position_Dec.phys / 40000 )
    #        return (actual_position_Dec.phys / factor)
    #


if __name__ == '__main__':
    network = canopen.Network()
    network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
    # Add some nodes with corresponding Object Dictionaries
    _node = canopen.RemoteNode(1, 'EcoVARIO_114_214_414.eds')
    network.add_node(_node)
    m = Motor(_node)
    #m.relative_positioning(turns=1, velocity=0.1)
    m.test()
    # while (True):
    #
    #     if m.inquire_DIN6 == 34:
    #         print(m.inquire_DIN6)
    #         pos_value = m.turns * 360
    #         break
    # # pos_value = m.turns * 360
    # new_pos_value = (180 + pos_value) / 360
    #
    # m.absolute_positioning(turns=1, velocity=0.5)
    # m.home_to_switch()
    #

    #while(1):
     #print(m.inquire_DIN6())

    #m.absolute_positioning(turns=10, velocity=1)
    #m.relative_positioning(turns=10, velocity=1)
    #time.sleep(1)
    #print(m.operating_mode)
    #m.absolute_positioning(turns=10, velocity=0)
    #time.sleep(1)
    #m.absolute_positioning(turns=10, velocity=1)
    #m.inquire_statusword()
    #print(m.status)

    #m.absolute_positioning(turns=10, velocity=1)

    #m.init()
    #m.status()
    #m.velocity1()
    #m.run_n_turns(turns=10, velocity=.5)
    #time.sleep(2)
    #m.stop()

    #time.sleep(2)
    #print(m.velocity)
    #m.velocity1()
    #time.sleep(10)
    #print(m.status)
    #print(m.turns)

    #m.halt()
#    #m.Homing()
    #m.init()
    # m.velocity_mode(target_velocity=1)
    # time.sleep(3)
    # m.stop_velocity_mode()
    # time.sleep(2)
    # m.velocity_mode(target_velocity=1)
    # time.sleep(3)
    # m.stop_velocity_mode()
