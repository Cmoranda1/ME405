## @file closed_loop.py
#  This is a closed loop controller class. 
#  It is a generic controller that can ajdust an actuation signal while being called in a loop
#
#  @author Chris Moranda & Hanno Mueller
#
#  @data January 29, 2019

## A closed loop driver object
#  The class contains a constructor as well as a way to adjust the setpoint and gain

class Closed_Loop:

	## Constructor for the closed loop driver
	#
	#  This driver initializes an object and sets the setpoint to 0 and the gain to 0
	def __init__(self):

		## The setpoint destination you wish to reach
		self.setpoint = 0

		## The gain the controller will use
		self.propgain = 0
	
	## The main control function used
	#  This function is placed within a loop that reads the current position.
	#  The current position is then subtracted from the setpoint forming the "error"
	#  The error is then multiplied by the gain and returned as the "actuation"
	#  @param The current position to be used to calculate actuation
	def control(self, curr_pos):
		error = self.setpoint - curr_pos
		actuation = self.propgain * (error)
		return actuation 

	## This function sets the set point of the controller
	#  @param The setpoint to be used as a destination	
	def set_setpoint(self, setpoint):
		self.setpoint = setpoint
	
	## This function sets the gain of the controller
	#  @param The gain to be used by the controller	
	def set_cont_gain(self, cont_gain):
		self.propgain = cont_gain
