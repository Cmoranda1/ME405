import motor
import encoder
import bno055 as bn
import closed_loop as loop
import utime


imu = bn.BNO055(bn.ndof)
# while(1):
# 	utime.sleep_ms(200)
# 	x = imu.get_sensor_reading(bn.EULER_H)
# 	x = x/16
# 	y = imu.get_sensor_reading(bn.EULER_R)
# 	y = y/16
# 	z = imu.get_sensor_reading(bn.EULER_P)
# 	z = z/16
# 	print("Heading : " + str(x) + " Roll Val: " + str(y) + " Pitch Val: " + str(z))
cL = loop.Closed_Loop()
cL.set_setpoint(0)

while(1):
	#print("Enter a gain: ")
	gain_set = input()
	cL.set_cont_gain(float(gain_set))
	mot1 = motor.MotorDriver("A")
	last_time = utime.ticks_ms()
	times = []
	positions = []

	while(1):
		utime.sleep_ms(100)
		#times.append(utime.ticks_ms())
		#if(pos > 180):
			#pos = -1*(360 - pos)
		x = imu.get_sensor_reading(bn.EULER_H)
		x = x/16
		y = imu.get_sensor_reading(bn.EULER_R)
		y = y/16
		z = imu.get_sensor_reading(bn.EULER_P)
		z = z/16
		actuation = cL.control(y)
		print("Heading : " + str(x) + " \t Roll Val: " + str(y) + " \t Pitch Val: " + str(z))
		mot1.set_duty_cycle(actuation)
		last_time = utime.ticks_ms()


