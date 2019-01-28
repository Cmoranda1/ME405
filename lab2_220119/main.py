import motor
import encoder
import closed_loop as loop
import utime

cL = loop.Closed_Loop()
cL.set_setpoint(4000)

while(1):
	#print("Enter a gain: ")
	gain_set = input()
	cL.set_cont_gain(float(gain_set))
	mot1 = motor.MotorDriver()
	enc1 = encoder.Encoder("A")
	enc1.zero()
	last_time = utime.ticks_ms()
	times = []
	positions = []

	for x in range(300):
		utime.sleep_ms(10)
		times.append(utime.ticks_ms())
		pos = enc1.read()
		positions.append(pos)
		actuation = cL.control(pos)
		mot1.set_duty_cycle(actuation)
		last_time = utime.ticks_ms()

	starttime = times[0]
	i = 0
	for time in times:
		times[i] = time - starttime
		i += 1
		
	print(positions)
	print(times)
