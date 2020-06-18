import unittest
import sys
import logging
from importlib import import_module

# unittest is used for writing the test application
# sys and logging modules are for logging test info onto the terminal

class TestPopulations(unittest.TestCase):
    def setUp(self):
        self.sim = import_module("pyNN.carlsim")
        self.sim.setup(timestep=0.01, min_delay=1.0, netName = "test_populations", simMode = 0, logMode = 3, ithGPUs = 0, randSeed = 42)
        
    #assign silly values and expect the program to fail
    
    def test_createSpikeGeneretorDeath(self):
        log = logging.getLogger("TestLog")
        log.debug("Testing Izhikevich population")

        with self.assertRaises(Exception, msg="negative values were supposed to raise an exception"):
            nNeur = -1
            spikeSource = self.sim.SpikeSourceArray([1,2,3,4,5,6,7,8])
            self.sim.Population(nNeur, spikeSource)

        with self.assertRaises(Exception, msg="negative values were supposed to raise an exception"):
            nNeur = (-1,1,1)
            spikeSource = self.sim.SpikeSourceArray([1,2,3,4,5,6,7,8])
            self.sim.Population(nNeur, spikeSource)
        with self.assertRaises(Exception, msg="negative values were supposed to raise an exception"):
            nNeur = (1,-1,1)
            spikeSource = self.sim.SpikeSourceArray([1,2,3,4,5,6,7,8])
            self.sim.Population(nNeur, spikeSource)
        with self.assertRaises(Exception, msg="negative values were supposed to raise an exception"):
            nNeur = (1,1,-1)
            spikeSource = self.sim.SpikeSourceArray([1,2,3,4,5,6,7,8])
            self.sim.Population(nNeur, spikeSource)

        with self.assertRaises(Exception, msg="negative values were supposed to raise an exception"):
            nNeur = (1,1,-1)
            spikeSource = self.sim.SpikeSourceArray([1,-2,3,4,5,6,7,8])
            self.sim.Population(nNeur, spikeSource)

        with self.assertRaises(Exception, msg="negative values were supposed to raise an exception"):
            nNeur = (1,1,-1)
            spikeSource = self.sim.SpikeSourceArray([1,10,3,4,5,6,7,8])
            self.sim.Population(nNeur, spikeSource)

        log.debug("Success")
        
        
    
    #set silly values
    #for now unable to write tests for neuron type
    def test_createGroup(self):
        log = logging.getLogger("TestLog")
        log.debug("Testing spike generator population")
        with self.assertRaises(Exception):
            self.sim.Population(-10, self.sim.Izhikevich("EXCITATORY_NEURON",a=0.02, b=0.2, c=-65, d=6, i_offset=[0.014, 0.0, 0.0]))
        
        with self.assertRaises(Exception):
            self.sim.Population((-10,1,1), self.sim.Izhikevich("EXCITATORY_NEURON",a=0.02, b=0.2, c=-65, d=6, i_offset=[0.014, 0.0, 0.0]))

        with self.assertRaises(Exception):
            self.sim.Population((10,-1,1), self.sim.Izhikevich("EXCITATORY_NEURON",a=0.02, b=0.2, c=-65, d=6, i_offset=[0.014, 0.0, 0.0]))

        with self.assertRaises(Exception):
            self.sim.Population((10,1,-1), self.sim.Izhikevich("EXCITATORY_NEURON",a=0.02, b=0.2, c=-65, d=6, i_offset=[0.014, 0.0, 0.0]))

        with self.assertRaises(Exception):
            self.sim.Population(10, self.sim.Izhikevich("EXCITATORY_NEURON",a="a", b=0.2, c=-65, d=6, i_offset=[0.014, 0.0, 0.0]))

        with self.assertRaises(Exception):
            self.sim.Population(10, self.sim.Izhikevich("EXCITATORY_NEURON",a=0.02, b="a", c=-65, d=6, i_offset=[0.014, 0.0, 0.0]))

        with self.assertRaises(Exception):
            self.sim.Population(10, self.sim.Izhikevich("EXCITATORY_NEURON",a=0.02, b=0.2, c="a", d=6, i_offset=[0.014, 0.0, 0.0]))

        with self.assertRaises(Exception):
            self.sim.Population(10, self.sim.Izhikevich("EXCITATORY_NEURON",a=0.02, b=0.2, c=-65, d="a", i_offset=[0.014, 0.0, 0.0]))
    
        log.debug("success")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    #unittest.TextTestRunner().run(TestPopulations())
    unittest.main()