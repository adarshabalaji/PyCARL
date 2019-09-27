import numpy
from carlsim import *
from pyNN import common
from . import simulator
from .standardmodels.synapses import StaticSynapse

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
        common.Projection.__init__(self, presynaptic_population, postsynaptic_population,
                                   connector, synapse_type, source, receptor_type,
                                   space, label)

        if (receptor_type == "excitatory"):
            self.receptor_type = EXCITATORY_NEURON




