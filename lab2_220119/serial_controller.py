import serial
import time
ser = serial.Serial('COM3', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
print("Serial connection opened")
time.sleep(2)
ser.write(b"\x17")     # write a string#write something to serial port
time.sleep(2)
print("reboot")
time.sleep(5)#wait for reboot
ser.write(b"\x0D")
ser.write(b"\x0A")
#ser.write(b"\r\n")
#s = ser.read(100)        # read up to ten bytes (timeout) read answer back
s = ser.read(500)        # read up to ten bytes (timeout) read answer back
print("serial reading done")
print(str(s))#print 
print("serial flushed")
ser.flush()#cleans up serial buffer
ser.reset_output_buffer()
ser.reset_input_buffer()
ser.close()
