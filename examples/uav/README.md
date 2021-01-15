# Example of Drones integration using CoppeliaSim

Download CoppeliSim, you can use the script:

```
./examples/uav/install.sh
```

## Centralized and adhoc modes

This example can run as a centralized or adhoc mode. 

Start the network ad hoc scenario with the command below:

```
sudo python examples/uav/drone.py
```

This will start mn-wifi and the simulation in CoppeliaSim.

In parallel, it will start the remote API capturing the drones' position in the simulation and read the drones' positions to set the position of the stations.

In the mininet graph, you can see that the stations' position is updated according to the drones.

To verify the Drones' position in the simulation, run the `getstaposition.py` script with the station name (Only one station supported).

For example, to verify the position of sta1 (Drone1) run:

```
sudo python examples/uav/getstaposition.py sta1		
```
To see the position of all the drones, no pass any argument.


---
**NOTE**

If there is an error to connect to CoppeliaSim socket, run:
		
```
sudo pkill -9 -f python
```

If CoppeliaSim continue runing after finishing mininet-wifi execution, run:

```
sudo pkill -9 -f coppeliaSim
```
---
