# Example of Drones integration using CoppeliSim

Download CoppeliSim and untar in this folder (examples/uav/)
https://www.coppeliarobotics.com/files/CoppeliaSim_Edu_V4_1_0_Ubuntu18_04.tar.xz

## Centralized mode

To run this example as a centralized mode, you will need 3 terminals.

In terminal 1 run:

		sudo python examples/uav/uav_centralized.py

This will start mn-wifi and the simulation in CoppeliaSim.

In Terminal 2 run:

		sudo python examples/uav/simpleTest.py centralized

This will start the remote API capturing the position of the drones in the simulation.

In Terminal 3 run:

		sudo python examples/uav/setstaposition.py

This will read the positions of the drones and set the position of the stations.

In the mininet graph, you can see that the stations' position is updated according to the drones.

## adhoc mode

To run this example as adhoc mode, you will need 2 terminals.

In terminal 1 run:

		sudo python examples/uav/uav_adhoc.py 

This will start mn-wifi and the simulation in CoppeliaSim.

Then run

		mininet-wifi> xterm api1

In the new xterm terminal run:

		python examples/uav/simpleTest.py adhoc

This will start the remote API capturing the position of the drones in the simulation.

In Terminal 2 run:

		sudo python examples/uav/setstaposition.py

This will read the positions of the drones and set the position of the stations.

In the mininet graph, you can see that the stations' position is updated according to the drones.

---
**NOTE**
If there is an error to connect to CoppeliaSim socket, run sudo pkill -9 -f python
---
