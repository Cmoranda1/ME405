# main.py -- put your code here!
import pyb

class MotorDriver:
	''' This class implements a motor driver for the
	ME405 board. '''
	def __init__ (self):
		''' Creates a motor driver by initializing GPIO
		pins and turning the motor off for safety. '''
	
		#initialize pins
		self.EN_A = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
		self.IN1A = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
		self.IN2A = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
		
		#set all pins low
		self.EN_A.high()
		self.IN1A.low()
		self.IN2A.low()
		
		self.tim3 = pyb.Timer(3, freq=20000)
		self.ch1 = self.tim3.channel(1, pyb.Timer.PWM, pin=self.IN1A)
		self.ch2 = self.tim3.channel(2, pyb.Timer.PWM, pin=self.IN2A)
		
		#print ('Creating a motor driver')
	def set_duty_cycle (self, level):
		''' This method sets the duty cycle to be sent
		to the motor to the given level. Positive values
		cause torque in one direction, negative values
		in the opposite direction.
		@param level A signed integer holding the duty
		cycle of the voltage sent to the motor '''
		
		if(level > 100):
			level = 100
		elif(level < -100):
			level = -100
		
		#print ('Setting duty cycle to ' + str (level))
		
		#direction
		if level>0:		
			self.ch1.pulse_width_percent(abs(level))
			self.ch2.pulse_width_percent(0)
			#print('Positive Spin ' + str(level))
		elif level == 0:
			self.ch1.pulse_width_percent(abs(level))
			self.ch2.pulse_width_percent(abs(level))
			#print('motor is off')
		else:		
			self.ch1.pulse_width_percent(0)
			self.ch2.pulse_width_percent(abs(level))
			#print('Negative Spin ' + str(level))
