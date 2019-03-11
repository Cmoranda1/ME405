# -*- coding: utf-8 -*-
#
## @privatesection - Stuff in this file doesn't need to be Doxygen-ed
#
#  @author jr

import pyb
import micropython
import gc
import cotask
import task_share
import print_task
import busy_task
import motor
import encoder
import closed_loop as loop
import utime
import bno055 as bn
# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)


GOING = const (0)
STOPPED = const (1)

def task1_pitch_motor ():
    ## Function that implements task 1, a task which runs the closed loop motor control
    #  based on pitch readings from the IMU
    cL = loop.Closed_Loop()
    cL.set_setpoint(0)
    cL.set_cont_gain(2.4)
    mot1 = motor.MotorDriver("A")
	
    while True:
        #print("task 1")
        curr_pos = q2.get()
        #print(str(curr_pos))
        actuation = cL.control(curr_pos)
        q4.put(actuation)
        mot1.set_duty_cycle(actuation)
        yield(0)
		
def task2_roll_motor():
    ## Function that implements task 2, a task which runs the closed loop motor control
    #  based on roll readings from the IMU
    cL = loop.Closed_Loop()
    cL.set_setpoint(0)
    cL.set_cont_gain(2.4)
    mot2 = motor.MotorDriver("B")
    
    while True:
        #print("task2")
        ## if numbers in queue are available
        ## store value in variable curr_pos
        curr_pos = q3.get()
        #print(str(curr_pos))
        actuation = cL.control(curr_pos)
        q5.put(actuation)
        mot2.set_duty_cycle(actuation)
        yield(0)
		
def task3_imu_read():
    ## task for IMU pitch and roll values
    imu = bn.BNO055(bn.ndof)
    while True:
        #print("task3")
        q2.put(imu.get_sensor_reading(bn.EULER_P)/16)
        q3.put(imu.get_sensor_reading(bn.EULER_R)/16)
        yield(0)

def task4_print_stats():
    pitch = q2.get()
    roll  = q3.get()
    mot1  = q4.get()
    mot2  = q5.get()

    print(str(utime.ticks_ms()) + ", " + str(pitch) + ", " + str(roll) + ", " + str(mot1) + ", " + str(mot2))
		
# =============================================================================

if __name__ == "__main__":

    print ('\033[2JTesting scheduler in cotask.py\n')

    # Create a share and some queues to test diagnostic printouts

    ## Hold pitch values
    q2 = task_share.Share('f', thread_protect = False, name = "Queue_2")

    ## Hold roll values
    q3 = task_share.Share('f', thread_protect = False, name = "Queue_3")

    ## Hold pitch motor values
    q4 = task_share.Share('f', thread_protect = False, name = "Queue_4")

    ## Hold roll motor values
    q5 = task_share.Share('f', thread_protect = False, name = "Queue_5")
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed

    task1 = cotask.Task (task1_pitch_motor, name = 'Task_1', priority = 2,
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (task2_roll_motor, name = 'Task_2', priority = 2,
                         period = 10, profile = True, trace = False)
    task3 = cotask.Task (task3_imu_read, name = 'Task_3', priority = 2,
                         period = 20, profile = True, trace = False)
    task4 = cotask.Task (task4_print_stats, name = 'Task_4', priority = 1, 
                         period = 50, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task4)

    # A task which prints characters from a queue has automatically been
    # created in print_task.py; it is accessed by print_task.put_bytes()

    # Create a bunch of silly time-wasting busy tasks to test how well the
    # scheduler works when it has a lot to do

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is sent through the serial por
    #vcp = pyb.USB_VCP ()
    #while not vcp.any ():
    while(1):
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    #vcp.read ()

    # Print a table of task data and a table of shared information data
    #print ('\n' + str (cotask.task_list) + '\n')
    #print (task_share.show_all ())
    #print (task1.get_trace ())
    #print ('\r\n')
