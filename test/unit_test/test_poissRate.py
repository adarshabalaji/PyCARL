import unittest
import pyNN.carlsim as sim
from pyNN.carlsim.carlsim import Grid3D
class testPoissonRate(unittest.TestCase):
   
    def setUp(self):
        sim.setup(timestep=0.01, min_delay=1.0, netName = "LIF test", simMode = 0, logMode = 3, ithGPUs = 0, randSeed = 42)
   
    def tearDown(self):
        del sim.state.network

    def testSetPoissonRate(self):
        nNeur = 100
        cell = sim.SpikeSourcePoisson(neuronType = "EXCITATORY_NEURON", rate = 42)

        p1 = sim.Population(nNeur, cell)
        sim.state.setupNetwork()
        self.assertEqual(nNeur, sim.state.rateObjects[0].getNumNeurons())
        self.assertEqual(sim.state.rateObjects[0].getRates(), tuple([42.0]*100))

