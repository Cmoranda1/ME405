## @file closed_loop.py
#
#  This class creates a closed loop controller
#  The controller returns actuation values based on
#  a proportional and integral value
#  @authors Hanno Mueller and Chris Moranda
#
#  @date March 1 2019

class Closed_Loop:
    
    ## Constructor used to create a Closed_Loop object
    #  all values are initially set to zero
    def __init__(self):
        ## Setpoint that the controller would like to be at
        self.setpoint = 0
        ## The proportional gain, determined by current position - set point
        self.propgain = 0
        ## The integral part of the gain, calculated over time (e.g. a longer time away from the
        #  Setpoint is corrected by a larger torque/actuation
        self.intgain = 0
        ## The error sum, this is the delta part of the integral gain
        self.error_sum = 0
    
    ## Function that is run in a loop to perform control
    #  Integral is a running sum
    #  Proportion error is calculated by difference between current position and setpoint
    ## @param Current position of the system. This is calculated by some sensor that the
    #  control loop is monitoring
    def control(self, curr_pos):
        error = self.setpoint - curr_pos
        
        ## If someone holds the system in place, do not allow the
        #  integral gain to increase to a ridiculous amount and potentially
        #  break the system
        if(self.error_sum > 400):
            self.error_sum = 399
        elif(self.error_sum < -400):
            self.error_sum = -399
        
        self.error_sum += error
        actuation = self.propgain * (error) + self.intgain * self.error_sum
        
        return actuation
    
    ## Set setpoint for control
    ##  @param The desired setpoint
    def set_setpoint(self, set_point):
        self.setpoint = set_point
    ## Set both proportional and integral gain
    ## @param Proportional gain to use
    ## @param Integral gain to use
    def set_cont_gain(self, prop_gain, int_gain):
        self.propgain = prop_gain
        self.intgain = int_gain
