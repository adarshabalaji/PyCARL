import unittest
import pyNN.carlsim as sim
class testCore(unittest.TestCase):
    
    def setUp(self):
        sim.setup(timestep=0.01, min_delay=1.0, netName = "LIF test", simMode = 0, logMode = 3, ithGPUs = 0, randSeed = 42)
    def tearDown(self):
        del sim.state.network

    def testESTDPTrue(self):
        alphaPlus = 5.0
        alphaMinus = -10.0
        tauPlus = 15.0
        tauMinus = 20.0
        #These are the only parameters supported by the pyNN STDP API

        cell = sim.Izhikevich(neuronType = "EXCITATORY_NEURON", a = 0.02, b = 0.2, c = -65, d = 8)
        syn = sim.STDPMechanism(
                timing_dependence = sim.SpikePairRule(tauPlus, tauMinus, alphaPlus, alphaMinus),
                weight_dependence = sim.AdditiveWeightDependence(w_min = 0, w_max = 0.0001),
                weight = 2,
                delay = 1,
                dendritic_delay_fraction = 0)

        g1 = sim.Population(10, cell)
        c1 = sim.Projection(g1, g1, sim.AllToAllConnector(), syn)

        info = sim.state.network.getGroupSTDPInfo(g1.carlsim_group)
        self.assertTrue(info.WithSTDP)
        self.assertTrue(info.WithESTDP)
        self.assertTrue(info.WithESTDPtype == sim.STANDARD)
        self.assertTrue(info.WithESTDPcurve == sim.EXP_CURVE)

        self.assertEqual(info.ALPHA_PLUS_EXC, alphaPlus)
        self.assertEqual(info.ALPHA_MINUS_EXC, alphaMinus)
        self.assertAlmostEqual(info.TAU_PLUS_INV_EXC, 1.0/tauPlus)
        self.assertAlmostEqual(info.TAU_MINUS_INV_EXC, 1.0/tauMinus)


