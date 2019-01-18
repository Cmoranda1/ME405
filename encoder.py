import pyb

'''import encoder as enc
enc = encoder.Encoder()# creates encoder object
encoder1 = read()
wiring: blue=PB7 Yellow=PB6'''
MAX = 65535
class Encoder:
	'''This class implements an encoder class for the 
	ME-405 board '''
	def __init__(self, ENC_NUM):
		'''creates an encoder by initializing
		a timer and GPIO pins to read the channels
		The Parameter ENC_NUM specifies which pins to use if 
		multiple encoders are in use. An argument of "A" will 
		result in PB6 and PB7 being used. And argument of "B"
		will result in PC6 and PC7 being used to read the quadrature 
		signal'''
		
		if(ENC_NUM == 'A'):
			print('Encoder A created')
			self.tim = pyb.Timer(4)
			self.tim.init(prescaler=0, period=MAX)
			self.b6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
			self.b7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.b6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.b7)
		
		elif(ENC_NUM == 'B'):
			print('Encoder B created')
			self.tim = pyb.Timer(8)
			self.tim.init(prescaler=0, period=MAX)
			self.c6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
			self.c7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.c6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.c7)
		
		self.ENC_NUM = ENC_NUM #store Encoder-Number for zero-fctn
		self.offset = 0 #creates offset variable
		self.lastvalue = 0 #stores position of last reading
		self.absolute = 0
		
	def read(self):
		'''returns the current position
		substract offset value from last zero-position from value'''
		self.currentvalue = self.tim.counter()
		if (self.lastvalue - self.currentvalue > MAX/2):
			print("overflow happened!!")
			self.absolute += (MAX-self.lastvalue)+self.currentvalue
		elif (self.currentvalue - self.lastvalue > MAX/2):
			print("underflow happened!!")
			self.absolute -= (self.lastvalue + (MAX - self.currentvalue))
		else:
			self.absolute += (self.currentvalue - self.lastvalue)
			
		self.lastvalue = self.currentvalue
		print("Current value is " + str(self.currentvalue))
		print("Absolute value is " + str(self.absolute))
		
	def zero(self):
		'''stores current position to offset variable'''
		if(self.ENC_NUM == 'A'):
			print("reset timer 4")
			self.tim = pyb.Timer(4)
			self.tim.init(prescaler=0, period=MAX)
			self.b6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
			self.b7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.b6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.b7)
			
		if(self.ENC_NUM == 'B'):
			print("reset timer 8")
			self.tim = pyb.Timer(8)
			self.tim.init(prescaler=0, period=MAX)	
			self.c6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
			self.c7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
			self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=self.c6)
			self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=self.c7)
			
		self.lastvalue = 0
		self.absolute = 0
		+
âˆ’print('Zero: ' + str(self.tim.counter()))