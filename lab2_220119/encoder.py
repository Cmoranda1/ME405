## @file encoder.py
#  This file contains an Encoder class. The Encoder object has the ability to read the number of clicks from an encoder.
#  This code accounts for overflow and underflow on a 16-bit encoder
#  
#  To run this code you must have a compatible Nucleo STM-32 board
#  Use the 3v3 and GND pins of the board to connect the Red and Black encoder wires Respectively
#  Depending on which timer you want to use, you can either use Pins B6 and B7 or C6 and C7
#  From the Repl Line, you can import the module (e.g import encoder as enc)
#  You can then create an instance of an encoder class (e = enc.Encoder("A") would create an encoder on the B6 and B7 pins)
#  e.read() will give the current position
#  e.zero() will reset the position
#
#  @author Chris Moranda
#  @author Hanno Mueller

## This class creates an Encoder object with the __init__() function
#  The read() function will return the number of clicks the encoder has counted
#  The read() function has a 16-bit current value, but also stores a running value 
#  in the event of an overflow or underflow
#  The zero() function will reset the counter so that the encoder restarts its count

import pyb

## 16-bit max
MAX = 65535
class Encoder:

	## Creates an encoder by initializing
	#  a timer and GPIO pins to read the channels
	#  @param input The Parameter ENC_NUM specifies which pins to use if 
	#  multiple encoders are in use. An argument of "A" will 
	#  result in PB6 and PB7 being used. And argument of "B"
	#  will result in PC6 and PC7 being used to read the quadrature 
	#  signal
	
	def __init__(self, ENC_NUM):
		
		
		if(ENC_NUM == 'A'):
			print('Encoder A created')

			## initializes timer 4 for pb6 and pb7
			self.tim = pyb.Timer(4)
			self.tim.init(prescaler=0, period=MAX)

			## initializes pins pb6 and pb7 to read the quadrature signal
			self.b6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
			self.b7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)

			## sets channels to read from the timer
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.b6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.b7)
		
		elif(ENC_NUM == 'B'):
			print('Encoder B created')

			## initializes timer 8 for pc6 and pc7
			self.tim = pyb.Timer(8)
			self.tim.init(prescaler=0, period=MAX)

			## initializes pins pc6 and pc7 to read the quadrature signal
			self.c6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
			self.c7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)

			## sets channels to read from the timer
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.c6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.c7)
		
		## stores Encoder-Number for zero-fctn
		self.ENC_NUM = ENC_NUM 

		## stores position of last reading
		self.lastvalue = 0 

		## stores the absolute running value
		self.absolute = 0

	## Read will return the current position and the absolute position
	#  The current position will be a number between 0-65535 (16-bits) that is read by the encoder
	#  The absolute position will account for overflow and underflow and will keep a running total of clicks 
	#  Absolute position is not limited by 16-bits

	def read(self):

		## Takes the current value read from the encoder
		self.currentvalue = self.tim.counter()

		## Detects overflow and adds to the absolute total the actual distance from the last reading
		if (self.lastvalue - self.currentvalue > MAX/2):
			print("overflow happened!!-----------------------------------------------------------------------------")
			self.absolute += (MAX-self.lastvalue)+self.currentvalue

		## Detects underflow and subtracts from the absolute total the actual distance from the last reading
		elif (self.currentvalue - self.lastvalue > MAX/2):
			print("underflow happened!!----------------------------------------------------------------------------")
			self.absolute -= (self.lastvalue + (MAX - self.currentvalue))

		## If no overflow occurs, adjust the absolute by the difference from the last reading
		else:
			self.absolute += (self.currentvalue - self.lastvalue)
		
		## When absolute has been correctly adjusted, adjust the last value to reflect the most current reading	
		self.lastvalue = self.currentvalue

		print("Current value is " + str(self.currentvalue))
		print("Absolute value is " + str(self.absolute))
		return self.absolute
	## Zero will reinitialize all of the timers and zero out the storage variables	
	def zero(self):
		
		if(self.ENC_NUM == 'A'):
			print("reset timer 4")
			## initializes timer 4 for pb6 and pb7
			self.tim = pyb.Timer(4)
			self.tim.init(prescaler=0, period=MAX)

			## initializes pins pb6 and pb7 to read the quadrature signal
			self.b6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
			self.b7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)

			## sets channels to read from the timer
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.b6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.b7)
			
		if(self.ENC_NUM == 'B'):
			print("reset timer 8")
			## initializes timer 4 for pc6 and pc7
			self.tim = pyb.Timer(8)
			self.tim.init(prescaler=0, period=MAX)	

			## initializes pins pc6 and pc7 to read the quadrature signal
			self.c6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
			self.c7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)

			## sets channels to read from the timer
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.c6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.c7)
		
		## reset the values that are being adjusted
		self.lastvalue = 0
		self.absolute = 0
