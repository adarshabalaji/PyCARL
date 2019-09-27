from pyNN.standardmodels import synapses,build_translations
from ..carlsim import *
from ..simulator import state
from ..import simulator


class StaticSynapse(synapses.StaticSynapse):
    __doc__ = synapses.StaticSynapse.__doc__

    def __init__(self):
        pass
        #### the synaptic weight will be set in the connection itself please check if it is not the case


