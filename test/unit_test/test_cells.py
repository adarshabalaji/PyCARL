import unittest
import pyNN.carlsim as sim
from pyNN.carlsim.carlsim import RangeRmem
class testCells(unittest.TestCase):
    def setUp(self):
        sim.setup(timestep=0.01, min_delay=1.0, netName = "LIF test", simMode = 0, logMode = 3, ithGPUs = 0, randSeed = 123)
    def tearDown(self):
        del sim.state.network

    def testLIFNeuron(self):
        rates = [0.0, 0.0, 0.0, 0.0, 33.3, 58.8, 76.9, 90.9, 100.0, 111.1, 125.0] #From CARLsim unittest
        cell = sim.IF_cond_exp_gsfa_grr("EXCITATORY_NEURON", 10, 2, -50.0, -65.0, RangeRmem(5.0))
        izCell = sim.Izhikevich("EXCITATORY_NEURON", 0.02, 0.2, -65.0, 8.0)
        shape = (1,1,1)

        gLIF = sim.Population(shape, cell)
        gDummy = sim.Population(shape, izCell)

        sim.Projection(gLIF, gDummy, sim.AllToAllConnector(), sim.StaticSynapse(weight = 0.05, delay = 1))

        sim.state.network.setConductances(False)
        sim.state.network.setIntegrationMethod(sim.FORWARD_EULER, 1)
        sim.state.network.setupNetwork()

        smLIF = sim.state.network.setSpikeMonitor(gLIF.carlsim_group, "NULL")

        for i in range(0,11):
            current = [float(i)*0.8]
            sim.state.network.setExternalCurrent(gLIF.carlsim_group, current)
            smLIF.startRecording()
            sim.state.network.runNetwork(10, 0)
            smLIF.stopRecording()
            self.assertAlmostEqual(smLIF.getPopMeanFiringRate(), rates[i], delta = 0.5)
    def testSpikeSourceArray(self):
        spikeTimes = [13, 42, 99, 102, 200, 523, 738, 820, 821, 912, 989]
        nNeur = 5
        cell = sim.Izhikevich("EXCITATORY_NEURON", 0.02, 0.2, -65, 8)
        spike = sim.SpikeSourceArray("EXCITATORY_NEURON", spike_times = spikeTimes)

        g1 = sim.Population(1, cell)
        g0 = sim.Population(nNeur, spike)
        
        sim.state.network.setConductances(True)

        c0 = sim.Projection(g0, g1, sim.FixedProbabilityConnector(p_connect = 0.5), sim.StaticSynapse(weight = 0.01, delay = 1))

        sim.state.network.setupNetwork()
        sm = sim.state.network.setSpikeMonitor(g0.carlsim_group, "NULL")
        sm.startRecording()
        sim.state.network.runNetwork(1,0)
        sm.stopRecording()

        results = sm.getSpikeVector2D()
        print(results)
        self.assertEqual(len(results), 5)
        for neuron in results:
            self.assertEqual(neuron, tuple(spikeTimes))
