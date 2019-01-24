## @file mainpage.py
#  @mainpage Lab#1 Assignment
#  @authors Chris Moranda 
#  @authors Hanno Mueller 
#  @section intro Introduction
#  just a quick overview about some important facts: \n
#  - @ref Purpose 
#  - @ref Usage 
#  - @ref Testing 
#  - @ref Limitations 
#  - @ref Location 
#
#  @section Purpose
#  This is a driver class for a 16 bit encoder. The driver has the ability to take precise readings of the position of the encoder, accounting for overflow.
#
#  @section Usage
#  This class creates an Encoder object with the __init__() function \n
#  The read() function will return the number of clicks the encoder has counted \n
#  The read() function has a 16-bit current value, but also stores a running value 
#   in the event of an overflow or underflow \n
#  The zero() function will reset the counter so that the encoder restarts its count
#
#  @section Testing
#  This class has been tested mostly through the REPL line. We ensured that one revolution gave the expected number of clicks (4000). Then we accounted for overflow and underflow. We tested this by producing enough revolutions to cause an overflow. We printed to the cmd line when this occured. We then altered the absolute value to account for this. We used the same process to test overlow and to ensure that spinning the encoder in the opposite direction reduced the count.
#
#  @section Limitations 
#  The code does not appear to have any bugs currently, but it is very likely we will discover limitations through more extensive testing.
#
#  @section Location
#  this is the location: 
#  <a href="http://wind.calpoly.edu/hg/mecha02/file/ec86bd04891a/Lab1/encoder.py">http://wind.calpoly.edu/hg/mecha02/file/ec86bd04891a/Lab1/encoder.py</a>.

