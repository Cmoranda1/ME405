class Closed_Loop:
    def __init__(self):
        self.setpoint = 0
        self.propgain = 0
        self.intgain = 0
        self.error_sum = 0
    #print("Creating Closed Loop System")
    
    def control(self, curr_pos):
        #print("distance from setpoint:" + str(self.setpoint - curr_pos))
        error = self.setpoint - curr_pos
        if(self.error_sum > 400):
            self.error_sum = 399
        elif(self.error_sum < -400):
            self.error_sum = -399
        
        self.error_sum += error
        actuation = self.propgain * (error) + self.intgain * self.error_sum
        
        #print("Actuation is: " + str(actuation))
        
        return actuation
    
    def set_setpoint(self, set_point):
        self.setpoint = set_point
    #print("setpoint is set to: " + str(self.setpoint))
    
    def set_cont_gain(self, prop_gain, int_gain):
        self.propgain = prop_gain
        self.intgain = int_gain
#print("Gain is set to: " + str(self.propgain))
