import pyNN.carlsim as sim
import unittest
from math import sqrt

class TestConnections(unittest.TestCase):

    def setUp(self):
        sim.setup(timestep=0.01, min_delay=1.0, netName = "testAllToAll", simMode = 0, logMode = 3, ithGPUs = 0, randSeed = 42)
        self.shape = (2,3,4)
        self.size = self.shape[0] * self.shape[1] * self.shape [2]
        self.cell = sim.Izhikevich(a = 0.02, b = 0.2, c = -65.0, d = 8.0, neuronType = "EXCITATORY_NEURON")
        self.syn = sim.StaticSynapse(weight = 1.0, delay = 1)

    def tearDown(self):
        del sim.state.network

    def testAllToAllConnector(self):
        g0 = sim.Population(self.shape, self.cell)
        g1 = sim.Population(self.shape, self.cell)
        g2 = sim.Population(self.shape, self.cell)
        g3 = sim.Population(self.shape, self.cell)
        g4 = sim.Population(self.shape, self.cell)
        g5 = sim.Population(self.shape, self.cell)

        c0 = sim.Projection(g0, g0, sim.AllToAllConnector(), self.syn, "excitatory")
        c1 = sim.Projection(g1, g1, sim.AllToAllConnector(), self.syn, "excitatory", radius = (-1.0, 0.0, 0.0))
        c2 = sim.Projection(g2, g2, sim.AllToAllConnector(), self.syn, "excitatory", radius = (-1.0, 0.0, -1.0))
        c3 = sim.Projection(g3, g3, sim.AllToAllConnector(), self.syn, "excitatory", radius = (2.0, 3.0, 0.0))
        c4 = sim.Projection(g4, g4, sim.AllToAllConnector(), self.syn, "excitatory", radius = (0.0, 2.0, 3.0))
        c5 = sim.Projection(g5, g5, sim.AllToAllConnector(), self.syn, "excitatory", radius = (2.0, 2.0, 2.0))

        sim.state.network.setupNetwork()

        self.assertEqual(sim.state.network.getNumSynapticConnections(c0.connId), self.size * self.size)
        self.assertEqual(sim.state.network.getNumSynapticConnections(c1.connId), self.size * self.shape[0]) 
        self.assertEqual(sim.state.network.getNumSynapticConnections(c2.connId), self.size * self.shape[0] * self.shape[2])
        self.assertEqual(sim.state.network.getNumSynapticConnections(c3.connId), 144)
        self.assertEqual(sim.state.network.getNumSynapticConnections(c4.connId), 224)
        self.assertEqual(sim.state.network.getNumSynapticConnections(c5.connId), 320)
        

    def testOneToOneConnector(self):

        g0 = sim.Population(self.shape, self.cell)
        g1 = sim.Population(self.shape, self.cell)
        g2 = sim.Population(self.shape, self.cell)

        c0 = sim.Projection(g0, g0, sim.OneToOneConnector(), self.syn)
        c1 = sim.Projection(g1, g1, sim.OneToOneConnector(), self.syn, radius = (-1, 0, 0))
        c2 = sim.Projection(g2, g2, sim.OneToOneConnector(), self.syn, radius = (-1, 0, -1))

        sim.state.network.setupNetwork()

        self.assertEqual(sim.state.network.getNumSynapticConnections(c0.connId), self.size)
        self.assertEqual(sim.state.network.getNumSynapticConnections(c1.connId), self.size) 
        self.assertEqual(sim.state.network.getNumSynapticConnections(c2.connId), self.size) 

    def testFixedProbabilityConnector(self):
        g0 = sim.Population(self.shape, self.cell)
        g1 = sim.Population(self.shape, self.cell)
        g2 = sim.Population(self.shape, self.cell)
        g3 = sim.Population(self.shape, self.cell)
        g4 = sim.Population(self.shape, self.cell)
        g5 = sim.Population(self.shape, self.cell)

        prob = 0.2
        c0 = sim.Projection(g0, g0, sim.FixedProbabilityConnector(p_connect = prob), self.syn, "excitatory")
        c1 = sim.Projection(g1, g1, sim.FixedProbabilityConnector(p_connect = prob), self.syn, "excitatory", radius = (-1.0, 0.0, 0.0))
        c2 = sim.Projection(g2, g2, sim.FixedProbabilityConnector(p_connect = prob), self.syn, "excitatory", radius = (-1.0, 0.0, -1.0))
        c3 = sim.Projection(g3, g3, sim.FixedProbabilityConnector(p_connect = prob), self.syn, "excitatory", radius = (2.0, 3.0, 0.0))
        c4 = sim.Projection(g4, g4, sim.FixedProbabilityConnector(p_connect = prob), self.syn, "excitatory", radius = (0.0, 2.0, 3.0))
        c5 = sim.Projection(g5, g5, sim.FixedProbabilityConnector(p_connect = prob), self.syn, "excitatory", radius = (2.0, 2.0, 2.0))

        sim.state.network.setupNetwork()
        errorMargin = 7.5*sqrt(prob*(1-prob)*self.size) + 0.5
        self.assertAlmostEqual(sim.state.network.getNumSynapticConnections(c0.connId), prob * self.size * self.size, delta = errorMargin)
        self.assertAlmostEqual(sim.state.network.getNumSynapticConnections(c1.connId), prob * self.size * self.shape[0], delta = errorMargin) 
        self.assertAlmostEqual(sim.state.network.getNumSynapticConnections(c2.connId), prob * self.size * self.shape[0] * self.shape[2], delta = errorMargin)
        self.assertAlmostEqual(sim.state.network.getNumSynapticConnections(c3.connId), prob * 144, delta = errorMargin)
        self.assertAlmostEqual(sim.state.network.getNumSynapticConnections(c4.connId), prob * 224, delta = errorMargin)
        self.assertAlmostEqual(sim.state.network.getNumSynapticConnections(c5.connId), prob * 320, delta = errorMargin)
       
