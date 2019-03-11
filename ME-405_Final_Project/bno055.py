## @file bno055.py
#  This is a driver class for the bno055 IMU sensor
#  It allows the user to set a mode and take a reading from any of the 9 axes
#
#  @author Chris Moranda and Hanno Mueller
#
#  @date March 1st 2019

import pyb
import utime

## Address of the I2C bus
addr = 41
## Register to change the operational mode
op_reg = 0x3d
## Operation to turn on all sensors
ndof = 0x0c

imu = 0x08

## Registers to get values from sensors
#  Names should be self explanatory
ACC_DATA_X = 0x08
ACC_DATA_Y = 0x0A
ACC_DATA_Z = 0x0C
MAG_DATA_X = 0x0E
MAG_DATA_Y = 0x10
MAG_DATA_Z = 0x12
GYR_DATA_X = 0x14
GYR_DATA_Y = 0x16
GYR_DATA_Z = 0x18

EULER_H = 0x1A
EULER_R = 0x1C
EULER_P = 0x1E

class BNO055:

	## Constructor to create a bno055 object
	#  @param A mode of operation to run in
	#  This mode is written to the operation register
	#  NDOF operation will turn on all of the axes for reading
	#  Constructor initially makes a public I2C object that can be used throughout code
	def __init__(self, mode):
		self.i2c = pyb.I2C(1, pyb.I2C.MASTER)
		self.addr = pyb.I2C.scan(self.i2c)
		if self.i2c.is_ready(addr):
			self.i2c.mem_write(mode, addr, op_reg)

	## This function is a generic function to take a reading from any of the sensors
	#  @param The sensor reading to return (e.g ACC_DATA_X returns acceleration in the X-Axis)
	def get_sensor_reading(self, axis_register):
		## To get the reading, read 2 bytes from the address of the I2C and the specified register
		#  of the desired axis
		reading = self.i2c.mem_read(2, addr, axis_register)
		## Reading will contain a byte array.
		#  The first index is the least significant byte 
		#  and the second index contains the most significant byte
		#  Do some bit shifting to put them in one int
		lsb = reading[0]
		msb = reading[1]
		msb = msb << 8
		value = msb + lsb

		## The numbers are 16-bit 2's complement values
		#  If the MSB is set, then subtract 2^16 -1 to account for negative values
		if(value > 32767):
			value = value - 65535
		return value