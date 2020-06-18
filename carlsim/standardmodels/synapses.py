from pyNN.standardmodels import synapses,build_translations
from ..carlsim import *
from ..simulator import state
from ..import simulator


class StaticSynapse(synapses.StaticSynapse):
    __doc__ = synapses.StaticSynapse.__doc__



class STDPMechanism(synapses.STDPMechanism):
    __doc__ = synapses.STDPMechanism.__doc__
    
    initial_conditions = {"M": 0.0, "P": 0.0}

    def __init__(self, timing_dependence=None, weight_dependence=None,
                 voltage_dependence=None, dendritic_delay_fraction=1.0,
                 weight=0.0, delay=None):
        if dendritic_delay_fraction != 0:
            raise ValueError("The pyNN.carlsim backend does not currently support "
                             "dendritic delays: for the purpose of STDP calculations "
                             "all delays are assumed to be axonal.")
        
	# could perhaps support axonal delays using parrot neurons?
        super(STDPMechanism, self).__init__(timing_dependence, weight_dependence,
                                            voltage_dependence, dendritic_delay_fraction,
                                            weight, delay)

class SpikePairRule(synapses.SpikePairRule):
    __doc__ = synapses.SpikePairRule.__doc__


class AdditiveWeightDependence(synapses.AdditiveWeightDependence):
    __doc__ = synapses.AdditiveWeightDependence.__doc__


