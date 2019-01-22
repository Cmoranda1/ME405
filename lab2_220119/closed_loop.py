
class Closed_Loop:
	def __init__(self):
		self.setpoint = 0
		self.propgain = 0
		print("Creating Closed Loop System")
		
	def control(self, curr_pos):
		print("distance from setpoint:" + str(curr_pos - self.setpoint))
		error = curr_pos - self.setpoint
		actuation = self.propgain * (error)
		print("Actuation is: " + str(actuation))
		return actuation 
		
	def set_setpoint(self, setpoint):
		self.setpoint = setpoint
		print("setpoint is set to: " + str(self.setpoint))
		
	def set_cont_gain(self, cont_gain):
		self.propgain = cont_gain
		print("Gain is set to: " + str(self.propgain))