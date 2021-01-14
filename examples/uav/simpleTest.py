#!/usr/bin/python

# Make sure to have the server side running in CoppeliaSim
# Run setstaposition.py to update station location
# If there is an error to connect to the socket run sudo pkill -9 -f python

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys
import time
import socket
import os
from mn_wifi.net import Mininet_wifi


data_drone_1 = ""
data_drone_2 = ""
data_drone_3 = ""
    

def drone_position(args):

    global data_drone_1
    global data_drone_2
    global data_drone_3

    print ('Program started')
    sim.simxFinish(-1) # just in case, close all opened connections
    
    mode = str(sys.argv[1])


    if mode == 'centralized':
        print("Centralized mode")
        clientID=sim.simxStart('10.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
    elif mode == 'adhoc':
        print("adhoc mode")
        clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
    else:
        print("No mode defined")
        exit()

    if clientID!=-1:
        print ('Connected to remote API server')


        #Getting the ID of the drones from the simulation
        [res,drone]=sim.simxGetObjectHandle(clientID, 'Quadricopter_base', sim.simx_opmode_oneshot_wait);
        #[res,targetObj]=sim.simxGetObjectHandle(clientID, 'Quadricopter_target', sim.simx_opmode_oneshot_wait);

        [res,drone_2]=sim.simxGetObjectHandle(clientID, 'Quadricopter_base#0', sim.simx_opmode_oneshot_wait);
        #[res,targetObj_2]=sim.simxGetObjectHandle(clientID, 'Quadricopter_target#0', sim.simx_opmode_oneshot_wait);

        [res,drone_3]=sim.simxGetObjectHandle(clientID, 'Quadricopter_base#1', sim.simx_opmode_oneshot_wait);
        #[res,targetObj_3]=sim.simxGetObjectHandle(clientID, 'Quadricopter_target#1', sim.simx_opmode_oneshot_wait);

        res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
        if res==sim.simx_return_ok:
            print ('Running Simulation')
        else:
            print ('Remote API function call returned with error code: ',res)

        time.sleep(2)

        startTime=time.time()

        #Starting the getPosition function streaming
        sim.simxGetObjectPosition(clientID,drone,-1,sim.simx_opmode_streaming) # Initialize streaming
        sim.simxGetObjectPosition(clientID,drone_2,-1,sim.simx_opmode_streaming) # Initialize streaming
        sim.simxGetObjectPosition(clientID,drone_3,-1,sim.simx_opmode_streaming) # Initialize streaming
        while True:
            
            #Getting the positions as buffers
            returnCode,data=sim.simxGetObjectPosition(clientID,drone,-1,sim.simx_opmode_buffer) # Try to retrieve the streamed data
            returnCode_2,data_2=sim.simxGetObjectPosition(clientID,drone_2,-1,sim.simx_opmode_buffer)
            returnCode_3,data_3=sim.simxGetObjectPosition(clientID,drone_3,-1,sim.simx_opmode_buffer)

            #Printing the positions of the drones
            print ('Drone 1 position: ',data)
            print ('Drone 2 position: ',data_2)
            print ('Drone 3 position: ',data_3)

            #Creating the messages to set the position of the stations
            #Escalating the position by 20 to be easy to visualize in mininet
            data_drone_1 = "set.sta1.setPosition(\"" + str(50-data[0]*20) + "," + str(50-data[1]*20) + "," + str(50-data[2]*20) + "\")"
            data_drone_2 = "set.sta2.setPosition(\"" + str(50-data_2[0]*20) + "," + str(50-data_2[1]*20) + "," + str(50-data_2[2]*20) + "\")"
            data_drone_3 = "set.sta3.setPosition(\"" + str(50-data_3[0]*20) + "," + str(50-data_3[1]*20) + "," + str(50-data_3[2]*20) + "\")"

            #Storing the position in data files
            f = open("examples/uav/data/positions_1.txt", "w")
            f.write(data_drone_1)
            f.close()

            f = open("examples/uav/data/positions_2.txt", "w")
            f.write(data_drone_2)
            f.close()

            f = open("examples/uav/data/positions_3.txt", "w")
            f.write(data_drone_3)
            f.close()
             
            time.sleep(1)

        # Now close the connection to CoppeliaSim:
        sim.simxFinish(clientID)
    else:
        print ('Failed connecting to remote API server')
    print ('Program ended')


if __name__ == '__main__':
    drone_position(sys.argv)
