from copy import deepcopy
from pyNN.standardmodels import cells, build_translations
from ..import simulator
from ..carlsim import *


class Izhikevich(cells.Izhikevich):
    __doc__ = cells.Izhikevich.__doc__
    
    translations = build_translations(
        ('a',        'a'),
        ('b',        'b'),
        ('c',        'c'),
        ('d',        'd'),
        ('i_offset', 'I_e', 1000.0),
    )

class SpikeSourceArray(cells.SpikeSourceArray):
    __doc__ = cells.SpikeSourceArray.__doc__

    def __init__(self, neurName, number, type, conductances):

        if conductances == "CUBA":
            simulator.state.network.setConductances(False)
        if conductances == "COBA":
            simulator.state.network.setConductances(True)

            simulator.state.network.setConductances(False)

        if type=="EXCITATORY":
            carlsim_model = simulator.state.network.createSpikeGeneratorGroup(neurName, number,EXCITATORY_NEURON )
