## @file mainpage.py
#  @mainpage
#  @section authors Authors: Chris Moranda and Hanno Mueller
#  @section intro Introduction
#  This is the main page for the HC Woody project, an innovative self-balancing table
#  @section purpose Purpose
#  This design has a wide range of applications. Perhaps for a dinner table on a cruise ship,
#  or any other use where stabilization may be necessary.

## @file main.py
#  This file contains all of the task setup and control for 
#  HC Woody, the self balancing table
#  To run this code, it is essential to have included all of 
#  the driver libraries that are mentioned below, as well as 
#  utilizing the correct hardware and setting up the system as 
#  we have layed out in the design report
#
#  @author Chris Moranda
#  @author Hanno Mueller
#
#

import pyb
import micropython
import gc
import cotask
import task_share
import print_task
import busy_task
import motor
import encoder as enc
import closed_loop as loop
import utime
import bno055 as bn

# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)


#GOING = const (0)
STOPPED = const (1)

## This function is not for a task
#  it must be done before the tasks begin running, to ensure accurate values from the sensors
#  Using the serial terminal, the function will request that the table is level before beginning
#  The pin PA6 will then be turned on to power up the sensor, and therefore reset the Euler Angles
#  to 0 before beginning
def start_up_calibration():
    on_pin = pyb.Pin(pyb.Pin.board.PA6, pyb.Pin.OUT)
    on_pin.low()
    txt = input("Place the table flat for calibration")
    on_pin.high()

## Function that implements task 1, a task which runs the closed loop motor control
#  based on pitch readings from the IMU
def task1_pitch_motor ():
    ## Closed Loop object is created and used throughout
    cL = loop.Closed_Loop()
    ## Setpoint is set to 0, as this indicated the table being level
    cL.set_setpoint(0)
    ## The gains for our PI controller were determined through trial and error
    cL.set_cont_gain(3.7, 0.07)
    mot1 = motor.MotorDriver("A")
	
    while True:
        curr_pos = q2.get()
        actuation = cL.control(curr_pos)
        q4.put(actuation)
        if(abs(q9.get()) < 40):
            ## Normal range of motor, adjust angles
            mot1.set_duty_cycle(actuation)
        elif(q9.get() >= 40 and curr_pos > 5):
            ## Motor is back in a safe range, resume operation
            mot1.set_duty_cycle(actuation)
        elif(q9.get() <= -40 and curr_pos < -5):
            ## Motor is back in a safe range, resume operation
            mot1.set_duty_cycle(actuation)
        else:
            ## Motor is in danger of spinning past its physical limit
            #  Turn Motor OFF!
            mot1.set_duty_cycle(0)
        q6.put(cL.error_sum)
        yield(0)

## Function that implements task 2, a task which runs the closed loop motor control
#  based on roll readings from the IMU
def task2_roll_motor():
    ## Closed Loop object is created and used throughout
    cL = loop.Closed_Loop()
    ## Setpoint is set to 0, as this indicated the table being level
    cL.set_setpoint(0)
    ## The gains for our PI controller were determined through trial and error
    cL.set_cont_gain(3.7, 0.07)
    mot2 = motor.MotorDriver("B")
    
    while True:
        ## if numbers in queue are available
        ## store value in variable curr_pos
        curr_pos = q3.get()
        #print(str(curr_pos))
        actuation = cL.control(curr_pos)
        q5.put(actuation)
        mot2.set_duty_cycle(actuation)
        q7.put(cL.error_sum)
        yield(0)

## This task utilizes the BNO055 sensor to take the Pitch and Roll
#  Angles all in a single run		
def task3_imu_read():
    ## BNO055 object is created before while loop
    imu = bn.BNO055(bn.ndof)
    while True:
        ## The shared variable q2 holds the current Pitch Value
        q2.put(imu.get_sensor_reading(bn.EULER_P)/16)
        ## The shared variable q3 holds the current Roll Value
        q3.put(imu.get_sensor_reading(bn.EULER_R)/16)
        yield(0)

## This task was mostly used for debugging purposes
#  The task takes all of the current statistics and prints the, in a nice format
def task4_print_stats():
    pitch = 0
    roll = 0
    mot1 = 0
    mot2 = 0
    enc1 = 0
    enc2 = 0

    while True:
        pitch = q2.get()
        roll  = q3.get()
        mot1  = q4.get()
        mot2  = q5.get()
        error_sum1 = q6.get()
        error_sum2 = q7.get()
        enc1 = q8.get()
        enc2 = q9.get()

        print("%6d , %3.2f , %3.2f , %3.2f , %3.2f, %3.2f, %3.2f " % (utime.ticks_ms() , pitch , roll , mot1 , mot2, enc1, enc2))
 
        yield(0)

## This task was created to read from the encoders
#  It takes the readings of both encoders in a single run
def task5_read_encoder():
    enc1 = enc.Encoder("A")
    enc2 = enc.Encoder("B")
    while(1):
        ## The shared variable q8 holds the current position of the pitch motor
        q8.put(enc1.read())
        ## The shared variable q9 holds the current position of the roll motor
        q9.put(enc2.read())
        yield(0)
		
# =============================================================================

if __name__ == "__main__":



    # Create a share and some queues to test diagnostic printouts

    ## Hold pitch values
    q2 = task_share.Share('f', thread_protect = False, name = "Queue_2")

    ## Hold roll values
    q3 = task_share.Share('f', thread_protect = False, name = "Queue_3")

    ## Hold pitch motor values
    q4 = task_share.Share('f', thread_protect = False, name = "Queue_4")

    ## Hold roll motor values
    q5 = task_share.Share('f', thread_protect = False, name = "Queue_5")
   
    ## Hold pitch motor error_sum
    q6 = task_share.Share('f', thread_protect = False, name = "Queue_6")
    
    ## Hold roll motor error_sum
    q7 = task_share.Share('f', thread_protect = False, name = "Queue_7")
    
    ## Hold pitch encoder values
    q8 = task_share.Share('f', thread_protect = False, name = "Queue_8")
    
    ## Hold roll encoder values
    q9 = task_share.Share('f', thread_protect = False, name = "Queue_9")
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed

    ## Motor task should be run at least every 22ms for "real time" results
    task1 = cotask.Task (task1_pitch_motor, name = 'Task_1', priority = 2,
                         period = 22, profile = True, trace = False)
    ## Motor task should be run at least every 22ms for "real time" results
    task2 = cotask.Task (task2_roll_motor, name = 'Task_2', priority = 2,
                         period = 22, profile = True, trace = False)
    ## The IMU read task should as often as the motors to keep consistency between movement
    #  and current angles
    task3 = cotask.Task (task3_imu_read, name = 'Task_3', priority = 3,
                         period = 22, profile = True, trace = False)
    ## The print task stats has no bearing on the functionality of the system
    #  and therefore does not need a high priority or a fast timing
    task4 = cotask.Task (task4_print_stats, name = 'Task_4', priority = 1,
                         period = 50, profile = True, trace = False)
    ## The encoder task doesn't need to be called as often as the motor tasks, because the cutoff
    #  angle is less than the actual physical limit, so the range of error allows for a low priority
    task5 = cotask.Task (task5_read_encoder, name = 'Task_5', priority = 4,
                         period = 50, profile = True, trace = False)
                         
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task4)
    cotask.task_list.append (task5)

    # A task which prints characters from a queue has automatically been
    # created in print_task.py; it is accessed by print_task.put_bytes()

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is sent through the serial por

    start_up_calibration()
    utime.sleep_ms(2000)
    while(1):
        cotask.task_list.pri_sched ()


