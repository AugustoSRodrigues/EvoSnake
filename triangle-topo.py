# Import mininet related packages
#from mininet.net import Mininet
#from mininet.node import Node, RemoteController
#from mininet.log import setLogLevel, info
#from mininet.node import CPULimitedHost
#from mininet.link import TCLink
#from mininet.cli import CLI
from mininet.topo import Topo

class triang(Topo):
    def __init__(self):
        #Init topology
        Topo.__init__(self)

        # Create the network switches
        s1, s2, s3 = [self.addSwitch(s) for s in 's1', 's2', 's3']
  
        h1, h2, h3 = [self.addHost(h) for h in 'h1', 'h2', 'h3']

        # Add link between switches. Each link has a delay of 5ms and 10Mbps bandwidth
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)

        # Add link between a host and a switch
        for (h, s) in [(h1, s1), (h2, s2), (h3, s3)]:
            self.addLink(h, s)

topos = { "triang": (lambda: triang()) }