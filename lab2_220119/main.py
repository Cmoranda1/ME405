import motor
import encoder
import closed_loop as loop
import utime

cL = loop.Closed_Loop()
cL.set_setpoint(5000)
cL.set_cont_gain(0.01)
mot1 = motor.MotorDriver()
enc1 = encoder.Encoder("A")
mot1.set_duty_cycle(10)
last_time = utime.ticks_ms()
'''This isn't correct yet. You'll want to find a good gain to use, constantly read to see if you're at the 
correct position, call control to actuate etc...'''
while(1):
	if(utime.ticks_ms() > (last_time + 10)):
		enc1.read()
		cL.control(enc1.read())
		
		last_time = utime.ticks_ms()
		if(enc1.read() == cL.setpoint):
			break
mot1.set_duty_cycle(0)
		