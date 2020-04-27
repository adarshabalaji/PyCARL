import numpy
from carlsim import *
from pyNN import common
from . import simulator
from .standardmodels.synapses import StaticSynapse

from pyNN.connectors import AllToAllConnector,OneToOneConnector,FixedProbabilityConnector        

class Connection(common.Connection):
    def __init__(self, group_id1, group_id2, connection_type, syn_wt_type, delay):
        self.group_id1 = group_id1
        self.group_id2 = group_id2
        self.connection_type = connection_type
        self.syn_wt_type = syn_wt_type
        self.delay = delay

class Projection(common.Projection):
    __doc__ = common.Projection.__doc__
    _simulator = simulator
    _static_synapse_class = StaticSynapse

    def __init__(self, presynaptic_population, postsynaptic_population,
                 connector, synapse_type=None, source=None, receptor_type=None,
                 space=None, label=None):
 #       common.Projection.__init__(self, presynaptic_population, postsynaptic_population,
  #                                 connector, synapse_type, source, receptor_type,
   #                                space, label)

        if isinstance(connector, OneToOneConnector):
            simulator.state.network.connect(presynaptic_population.carlsim_group, postsynaptic_population.carlsim_group, "one-to-one",
                    RangeWeight(1), 0, RangeDelay(1), RadiusRF(-1), SYN_FIXED)

        if isinstance(connector, AllToAllConnector):
            simulator.state.network.connect(presynaptic_population.carlsim_group, postsynaptic_population.carlsim_group, "full",
                    RangeWeight(1), 0, RangeDelay(1), RadiusRF(-1), SYN_FIXED)
        
        if isinstance(connector, FixedProbabilityConnector):
            simulator.state.network.connect(presynaptic_population.carlsim_group, postsynaptic_population.carlsim_group, "random", RangeWeight(1),
                    connector.p_connect, RangeDelay(1,20), RadiusRF(-1), SYN_PLASTIC)
