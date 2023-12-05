#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False )


    info( '*** Add switches\n')
    s1 = net.addHost('s1', cls=Node, ip=None)
    s2 = net.addHost('s2', cls=Node, ip=None)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip=None, mac='00:00:10:10:00:01')
    h2 = net.addHost('h2', cls=Host, ip=None, mac='00:00:10:10:00:02')
    h3 = net.addHost('h3', cls=Host, ip=None, mac='00:00:10:10:00:03')
    h4 = net.addHost('h4', cls=Host, ip=None, mac='00:00:10:10:00:04')

    info( '*** Add links\n')
    #net.addLink(s1, h1, 0, 0)
    Link(s1, h1, intfName1='s1-eth0')
    #net.addLink(s1, h2, 1, 0)
    Link(s1, h2, intfName1='s1-eth1')
    #net.addLink(s1, h3, 2, 0)
    Link(s1, h3, intfName1='s1-eth2')
    
    Link(s1, s2, intfName1='s1-eth3', intfName2='s2-eth0')
    Link(s2, h4, intfName1='s2-eth1')




    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    info( '*** Turn off IPv6\n')
    s1.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    s1.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    s2.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    s2.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h1.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h1.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h2.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h2.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h3.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h3.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h4.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h4.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')


    h1.cmd('ip addr add 10.0.0.1/24 dev h1-eth0')
    h2.cmd('ip addr add 10.0.0.1/24 dev h2-eth0')
    h3.cmd('ip addr add 10.0.0.1/24 dev h3-eth0')
    h4.cmd('ip addr add 10.0.0.1/24 dev h4-eth0')


    s1.cmd('ip link add br0 type bridge')
    s1.cmd('ip link set s1-eth0 master br0')
    s1.cmd('ip link set s1-eth1 master br0')
    s1.cmd('ip link set s1-eth2 master br0')
    s1.cmd('ip link set br0 up')


    s2.cmd('ip link add br0 type bridge')
    s2.cmd('ip link set s1-eth0 master br0')
    s2.cmd('ip link set s1-eth1 master br0')
    s2.cmd('ip link set br0 up')


    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
