from gpiozero import LED


class Arrow:
    ''' Defines an object for controlling one of the LED arrows on the Motorshield.

        Arguments:
        which = integer label for each arrow. The arrow number if arbitrary starting with:
            1 = Arrow closest to the Motorshield's power pins and running clockwise round the board
            ...
            4 = Arrow closest to the motor pins.
    '''
    arrowpins = {1: 13, 2: 19, 3: 26, 4: 16}  # GPIO pin numbers

    def __init__(self, which):
        self.pin = self.arrowpins[which]
        self.led = LED(self.pin)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()



from gpiozero import PWMOutputDevice, DigitalOutputDevice


class Motor:
    ''' Class to handle interaction with the motor pins
    Supports redefinition of "forward" and "backward" depending on how motors are connected
    Use the supplied Motorshieldtest module to test the correct configuration for your project.

    Arguments:
    motor = string motor pin label (i.e. "MOTOR1","MOTOR2","MOTOR3","MOTOR4") identifying the pins to which
            the motor is connected.
    config = int defining which pins control "forward" and "backward" movement.
    '''
    motorpins = {"MOTOR4": {"config": {1: {"e": 12, "f": 8, "r": 7}, 2: {"e": 12, "f": 7, "r": 8}}, "arrow": 1},
                 "MOTOR3": {"config": {1: {"e": 13, "f": 19, "r": 26}, 2: {"e": 13, "f": 26, "r": 19}}, "arrow": 2},
                 "MOTOR2": {"config": {1: {"e": 18, "f": 23, "r": 24}, 2: {"e": 18, "f": 24, "r": 23}}, "arrow": 3},
                 "MOTOR1": {"config": {1: {"e": 17, "f": 27, "r": 22}, 2: {"e": 17, "f": 22, "r": 27}}, "arrow": 4}}

    def __init__(self, motor, config):
        self.arrow_forward = Arrow(3)
        self.arrow_reverse = Arrow(1)
        self.pins = self.motorpins[motor]["config"][config]
        self.enable = PWMOutputDevice(self.pins['e'])
        self.forward_pin = DigitalOutputDevice(self.pins['f'])
        self.reverse_pin = DigitalOutputDevice(self.pins['r'])


    def forward(self, speed):
        ''' Starts the motor turning in its configured "forward" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 1.
        0 - stop and 1 - maximum speed
        '''
        print("Forward")
        self.enable.value = speed
        self.forward_pin.on()
        self.reverse_pin.off()
        self.arrow_reverse.off()
        self.arrow_forward.on()

    def reverse(self, speed):
        ''' Starts the motor turning in its configured "reverse" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 1.
        0 - stop and 1 - maximum speed
        '''
        print("Reverse")
        self.enable.value = speed
        self.forward_pin.off()
        self.reverse_pin.on()
        self.arrow_forward.off()
        self.arrow_reverse.on()

    def stop(self):
        print("Stop")
        self.enable.value = 0
        self.forward_pin.off()
        self.reverse_pin.off()
        self.arrow_forward.off()
        self.arrow_reverse.off()

# Example usage:
if __name__ == "__main__":
    import time

    motor = Motor("MOTOR1", 1)
    motor.forward(0.5)
    time.sleep(2)
    motor.reverse(0.5)
    time.sleep(2)
    motor.stop()

