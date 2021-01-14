# Example of Drones integration using CoppeliSim

Download CoppeliSim, you can use the script:

		./examples/uav/install.sh

## Centralized and adhoc modes

This example can run as a centralized or adhoc mode. 

Start mininet-wifi and select the corresponding mode as an argument (e.g., centralized, adhoc). 

For example, you can run the centralized scenario with the command:

		sudo python examples/uav/drone.py centralized

Or the adhoc scenario with the command:

		sudo python examples/uav/drone.py adhoc

This will start mn-wifi and the simulation in CoppeliaSim.

In parallel, it will start the remote API capturing the position of the drones in the simulation and read the positions of the drones to set the position of the stations.

In the mininet graph, you can see that the stations' position is updated according to the drones.

---
**NOTE**

If there is an error to connect to CoppeliaSim socket, run:
		
		sudo pkill -9 -f python

If CoppeliaSim continue runing after finishing mininet-wifi execution, run:

		sudo pkill -9 -f coppeliaSim
---
