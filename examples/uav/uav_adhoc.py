

#!/usr/bin/python

'Setting position of the nodes and enable sockets'

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.telemetry import telemetry
from mn_wifi.link import wmediumd, adhoc
import time
import os


def topology():

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   position='30,60,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8',
                   position='70,30,0')

    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8',
                   position='10,20,0')

    api1 = net.addStation('api1', mac='00:00:00:00:00:05', ip='10.0.0.5/8',
                   position='50,50,0')

    #ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
    #                         failMode="standalone", position='50,50,0')
    #h1 = net.addHost('h1', ip='10.0.0.1/8')

    #h2 = net.addHost('h2', ip='10.0.0.11/8')

    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    #net.addLink(ap1, h1)
    #net.addLink(ap1, h2)

    net.addLink(sta1, cls=adhoc, intf='sta1-wlan0',
            ssid='adhocNet', proto='batman_adv',
            mode='g', channel=5, ht_cap='HT40+')

    net.addLink(sta2, cls=adhoc, intf='sta2-wlan0',
            ssid='adhocNet', proto='batman_adv',
            mode='g', channel=5, ht_cap='HT40+')

    net.addLink(sta3, cls=adhoc, intf='sta3-wlan0',
            ssid='adhocNet', proto='batman_adv',
            mode='g', channel=5, ht_cap='HT40+')
    net.addLink(api1, cls=adhoc, intf='api1-wlan0',
            ssid='adhocNet', proto='batman_adv',
            mode='g', channel=5, ht_cap='HT40+')


    info("*** Starting network\n")
    #net.addNAT(linkTo='ap1').configDefault()
    net.build()
    #ap1.start([])

    nodes = net.stations
    telemetry(nodes=nodes, single=True, data_type='position')

    # # set_socket_ip: localhost must be replaced by ip address
    # # of the network interface of your system
    # # The same must be done with socket_client.py
    info("*** Starting Socket Server\n")
    net.socketServer(ip='127.0.0.1', port=12345)

    info("*** Running CLI\n")
    
    api1.cmd("./examples/uav/CoppeliaSim_Edu_V4_0_0_Ubuntu18_04/coppeliaSim.sh -s examples/uav/simulation.ttt -gGUIITEMS_2 &")

    time.sleep(10)
    
    #drone_position()

    CLI(net)

    info("*** Stopping network\n")
    net.stop()





if __name__ == '__main__':
    setLogLevel('info')
    topology()