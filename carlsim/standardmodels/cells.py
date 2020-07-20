from copy import deepcopy
from pyNN.standardmodels import cells, build_translations
from ..import simulator
from ..carlsim import *
import numpy as np
from pyNN import models


class IF_cond_exp_gsfa_grr(cells.IF_cond_exp_gsfa_grr):
    __doc__ = cells.IF_cond_exp_gsfa_grr.__doc__
    def __init__(self, neuronType, tau_m, tau_refrac, v_thresh, v_reset):
        if neuronType=='EXCITATORY_NEURON':                                                                                         self.type = EXCITATORY_NEURON
        elif neuronType=='INHIBITORY_NEURON':
            self.type = INHIBITORY_NEURON
        else:
            raise ValueError("Neuron type not supported by pyCARL")
        self.parameter_space = {'tau_m': tau_m, 'tau_refrac': tau_refrac, 'v_thresh': v_thresh, 'v_reset': v_reset}
        self.translations = build_translations(
                ('tau_m', 'tau_m'),
                ('tau_refrac', 'tau_ref'),
                ('v_thresh', 'vTh'),
                ('v_reset', 'vReset'),
        )


class Izhikevich(cells.Izhikevich):
    __doc__ = cells.Izhikevich.__doc__
    def __init__(self, neuronType, a, b, c, d):

        if neuronType=='EXCITATORY_NEURON':
            self.type = EXCITATORY_NEURON
        elif neuronType=='INHIBITORY_NEURON':
            self.type = INHIBITORY_NEURON
        else: 
            print("Neuron type not supported by pyCARL")
    
        self.parameter_space = {'a': a, 'b': b, 'c': c, 'd': d}

    translations = build_translations(
        ('a',        'a'),
        ('b',        'b'),
        ('c',        'c'),
        ('d',        'd'),
        ('i_offset', 'I_e', 1000.0),
    )


class SpikeSourceArray(cells.SpikeSourceArray):
    __doc__ = cells.SpikeSourceArray.__doc__
    neuronType = -1
    def __init__(self, neuronType, spike_times):

        if neuronType=='EXCITATORY_NEURON':
            self.type = EXCITATORY_NEURON
        elif neuronType=='INHIBITORY_NEURON':
            self.type = INHIBITORY_NEURON
        else: 
            print("Neuron type not supported by pyCARL")

        for x in spike_times:
            if (not isinstance(x, np.int64)):
                print("Spike times cannot be sub-millisecond precision")
                raise ValueError

        if isinstance(spike_times, np.ndarray):
            self.spike_times = spike_times.tolist()
        else:
            self.spike_times = spike_times

    

class SpikeSourcePoisson(cells.SpikeSourcePoisson):
    pars = cells.SpikeSourcePoisson.default_parameters
    
    def __init__(self, neuronType, rate = pars['rate']):
        self.rate = rate
        if neuronType=='EXCITATORY_NEURON':
            self.type = EXCITATORY_NEURON
        elif neuronType=='INHIBITORY_NEURON':
            self.type = INHIBITORY_NEURON
        else: 
            print("Neuron type not supported by pyCARL")


        #if (self.pars['duration'] != duration or self.pars['start'] != start):
        #print ("CARLsim does not support setting duration or start time for poisson objects. These parameters will be ignored")


class SpikeSourceVisualStimulus(models.BaseCellType):
    
    def __init__(self, image, neuronType):
        self.stim = simulator.VisualStimulus(image)
        self.size = (int(self.stim.getWidth()), int(self.stim.getHeight()), int(self.stim.getChannels()))
        self.length = self.stim.getLength()
        if neuronType=='EXCITATORY_NEURON':
            self.type = EXCITATORY_NEURON
        elif neuronType=='INHIBITORY_NEURON':
            self.type = INHIBITORY_NEURON
        else:
            print("Neuron type not supported by pyCARL")

    def getNextFrame(self, group, maxRate, minRate = 0.0):
        if (self.stim.getCurrentFrameNumber() >= self.length):
            print("Tried to get frame past end of file.")
            raise EOFError
        rates = self.stim.readFramePoisson(maxRate, minRate)
        simulator.state.network.setSpikeRate(group.carlsim_group, rates)
 
