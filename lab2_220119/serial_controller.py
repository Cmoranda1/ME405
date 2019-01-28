import serial
import time
from matplotlib import pyplot as plt

positions = []
position_list=[]
times = []
time_list = []
ser = serial.Serial('COM3', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
print("Serial connection opened")
time.sleep(2)
ser.write(b"0.045")
ser.write(b"\x0D")
ser.write(b"\x0A")
#ser.write(b"\r\n")
#s = ser.read(100)        # read up to ten bytes (timeout) read answer back
print("Waiting for test")
time.sleep(5)
s = ser.read(4000)        # read up to ten bytes (timeout) read answer back
print("serial reading done")
received=str(s)#convert bytes to char string
print(received)#print
#%%
pos_start = received.find("[")
pos_end = received.find("]")
time_start = received.rfind("[")
time_end = received.rfind("]")
pos_string = received[pos_start+1:pos_end]
time_string = received[time_start+1: time_end]
positions = pos_string.split(",")
times = time_string.split(",")
#%%
for pos in positions:
    position_list.append(int(pos))
for time_x in times:
    time_list.append(int(time_x))

plt.plot(time_list,position_list)
plt.xlabel('Time')
plt.ylabel('Motor_Position')
plt.show()

#%%
ser.flush()#cleans up serial buffer
ser.reset_output_buffer()
ser.reset_input_buffer()
print("serial flushed")
ser.close()
