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
	mot1 = motor.MotorDriver()
	last_time = utime.ticks_ms()
	times = []
	positions = []

	while(1):
		utime.sleep_ms(10)
		#times.append(utime.ticks_ms())
		pos = imu.get_sensor_reading(bn.EULER_H)
		pos = (pos/16) 
		if(pos > 180):
			pos = -1* (360 - pos)
		print(pos)
		#positions.append(pos)
		actuation = cL.control(pos)
		mot1.set_duty_cycle(actuation)
		last_time = utime.ticks_ms()

	#starttime = times[0]
	#i = 0
	#for time in times:
		#times[i] = time - starttime
		#i += 1
		
	#print(positions)
	#print(times)

# pos = []
# mot1 = motor.MotorDriver()
# enc1 = encoder.Encoder("A")
# enc1.zero()
# mot1.set_duty_cycle(50)
# for x in range(300):
# 	utime.sleep_ms(10)
# 	pos.append(enc1.read())
# mot1.set_duty_cycle(0)
# print(pos)
