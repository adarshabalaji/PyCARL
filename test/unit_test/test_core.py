import unittest
import pyNN.carlsim as sim
from pyNN.carlsim.carlsim import Grid3D
class testCore(unittest.TestCase):
    
    def setUp(self):
        sim.setup(timestep=0.01, min_delay=1.0, netName = "LIF test", simMode = 0, logMode = 3, ithGPUs = 0, randSeed = 42)
    def tearDown(self):
        del sim.state.network

    def testGrid3D(self):
        shape = (2,3,4)
        cell = sim.Izhikevich("EXCITATORY_NEURON", 0.02, 0.2, -65, 8)
        spike = sim.SpikeSourceArray("EXCITATORY_NEURON", spike_times = [1,2,3,4])
        g2 = sim.Population(shape, cell)
        g1 = sim.Population(shape, spike)
        c0 = sim.Projection(g1, g2, sim.AllToAllConnector(), sim.StaticSynapse(weight = 0.1, delay = 1))

        sim.state.network.setupNetwork()

        for idx in [g1.carlsim_group, g2.carlsim_group]:
            grid = sim.state.network.getGroupGrid3D(idx)
            self.assertEqual(grid.numX, shape[0])
            self.assertEqual(grid.numY, shape[1])
            self.assertEqual(grid.numZ, shape[2])
            self.assertEqual(grid.N, shape[0]*shape[1]*shape[2])
    
    def testSetWeights(self): #Currently does not support CUDA/GPU_MODE functionality
        spikeRates = []
        nNeur = 10
        cell = sim.Izhikevich("EXCITATORY_NEURON", 0.02, 0.2, -65, 8)
        g1 = sim.Population(nNeur, cell)
        c1 = sim.Projection(g1, g1, sim.AllToAllConnector(), sim.StaticSynapse(weight = 0.5, delay = 1))

        sim.state.network.setConductances(True)
        sim.state.network.setupNetwork()

        sm = sim.state.network.setSpikeMonitor(g1.carlsim_group, "NULL")
        sim.state.network.setExternalCurrent(g1.carlsim_group, 7)
        sm.startRecording()
        sim.state.network.runNetwork(2,0)
        sm.stopRecording()

        for i in range(0, 10):
            spikeRates.append(sm.getNeuronNumSpikes(i))
        c1.set(weight = 0)

        sm.startRecording()
        sim.state.network.runNetwork(2, 0)
        sm.stopRecording()

        for i in range(0,10):
            self.assertLess(sm.getNeuronNumSpikes(i), spikeRates[i])
