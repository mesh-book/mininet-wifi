#!/usr/bin/python

'Setting position of the nodes and enable sockets'

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.telemetry import telemetry
import time
import os
import sys

def topology(args):

    modes = ['centralized', 'adhoc']
    validmode = 0
    sta_drone = []

    if len(args) > 1:
        mode = str(args[1])
    else:
        print("No mode defined")
        exit()

    for mode_val in args:
        if mode_val in modes:
            mode = mode_val
            validmode = 1

    if validmode == 0:
        print("Mode not supprted, try centralized or adhoc")
        exit()

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8',
                   position='30,60,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',
                   position='70,30,0')

    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8',
                   position='10,20,0')

    if mode == 'centralized':
        print("Centralized mode")
        ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
                                 failMode="standalone", position='50,50,0')

    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()


    if mode == 'adhoc':
        print("adhoc mode")
        net.addLink(sta1, cls=adhoc, intf='sta1-wlan0',
                ssid='adhocNet', proto='batman_adv',
                mode='g', channel=5, ht_cap='HT40+')

        net.addLink(sta2, cls=adhoc, intf='sta2-wlan0',
                ssid='adhocNet', proto='batman_adv',
                mode='g', channel=5, ht_cap='HT40+')

        net.addLink(sta3, cls=adhoc, intf='sta3-wlan0',
                ssid='adhocNet', proto='batman_adv',
                mode='g', channel=5, ht_cap='HT40+')

    info("*** Starting network\n")
    if mode == 'centralized':
        net.addNAT(linkTo='ap1').configDefault()
    net.build()
    if mode == 'centralized':
        ap1.start([])

    if mode == 'centralized':
        nodes = net.stations + net.aps
    if mode == 'adhoc':
        nodes = net.stations

    telemetry(nodes=nodes, single=True, data_type='position')

    for n in net.stations:
        sta_drone.append(n.name)

    sta_drone_send = ' '.join(map(str, sta_drone)) 

    # # set_socket_ip: localhost must be replaced by ip address
    # # of the network interface of your system
    # # The same must be done with socket_client.py
    info("*** Starting Socket Server\n")
    net.socketServer(ip='127.0.0.1', port=12345)

    info("*** Running CLI\n")
    
    os.system('./examples/uav/CoppeliaSim_Edu_V4_1_0_Ubuntu18_04/coppeliaSim.sh -s examples/uav/simulation.ttt -gGUIITEMS_2 &')
    time.sleep(10)

    simpleTest = 'sudo python examples/uav/simpleTest.py ' + str(sta_drone_send) + ' &'
    os.system(simpleTest)

    setstaposition = 'sudo python examples/uav/setstaposition.py ' + str(sta_drone_send) + ' &'
    os.system(setstaposition)

    CLI(net)

    info("*** Stopping network\n")

    kill_process()
    net.stop()


def kill_process():
    os.system('sudo pkill -9 -f coppeliaSim')
    os.system('sudo pkill -9 -f simpleTest.py')
    os.system('sudo pkill -9 -f setstaposition.py')


    
if __name__ == '__main__':
    setLogLevel('info')
    
    # Killing old processes
    kill_process()

    topology(sys.argv)