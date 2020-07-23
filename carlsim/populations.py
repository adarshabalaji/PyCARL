import numpy
from pyNN import common
from pyNN.standardmodels import StandardCellType, cells
from pyNN.parameters import ParameterSpace, simplify
from . import simulator
from .recording import Recorder
from pyNN.carlsim.carlsim import *
from pyNN.carlsim.standardmodels.cells import SpikeSourceVisualStimulus

#synapse_type = ''

class Assembly(common.Assembly):
    __doc__ = common.Assembly.__doc__
    _simulator = simulator

class Population(common.Population):
    __doc__ = common.Population.__doc__
    _simulator = simulator
    _recorder_class = Recorder
    _assembly_class = Assembly

    def __init__(self, size, cellclass, cellparams=None, structure=None,
                             initial_values={}, label=None):
        self.shape = size
        common.Population.__init__(self, size, cellclass, cellparams, structure, initial_values, label)

    def _create_cells(self):
        id_range = numpy.arange(simulator.state.id_counter,
                                simulator.state.id_counter + self.size)
        self.all_cells = numpy.array([simulator.ID(id) for id in id_range],
                                     dtype=simulator.ID)
        self._mask_local = numpy.ones((self.size,), bool)
        for id in self.all_cells:
            id.parent = self
        simulator.state.id_counter += self.size
        if (isinstance(self.shape, int)):
            self.shape = self.shape
        elif (len(self.shape) == 2):
            self.shape = Grid3D(self.shape[0],self.shape[1], 1)
        elif (len(self.shape) == 3):
            self.shape = Grid3D(self.shape[0],self.shape[1],self.shape[2])
        else:
            print("really? How do you expect me to build a neural network in more than three dimensions?")
            raise ValueError
        if isinstance(self.celltype, cells.SpikeSourceArray):
            self.carlsim_group = simulator.state.network.createSpikeGeneratorGroup(str(self.label), self.shape, self.celltype.type) 
            spikeGen = SpikeGeneratorFromVector(self.celltype.spike_times)
            simulator.state.network.setSpikeGenerator(self.carlsim_group, spikeGen)
            simulator.state.rateObjects.append(spikeGen) #Need this so spikeGen doesn't go out of scope. Need a better solution
             
        elif isinstance(self.celltype, cells.Izhikevich):
            self.carlsim_group = simulator.state.network.createGroup(str(self.label), self.shape, self.celltype.type)
            parameters = self.celltype.parameter_space
            simulator.state.network.setNeuronParameters(self.carlsim_group, parameters['a'], parameters['b'],
                                                            parameters['c'], parameters['d'])
        elif isinstance(self.celltype, cells.SpikeSourcePoisson):
            self.carlsim_group = simulator.state.network.createSpikeGeneratorGroup(str(self.label), self.shape, self.celltype.type) 
            self._simulator.state.poissonObjects.append((self.carlsim_group, self.celltype.rate, self.size))
            self._simulator.state.groupIDs.append(self.carlsim_group)
        
        elif isinstance(self.celltype, SpikeSourceVisualStimulus):
            self.carlsim_group = simulator.state.network.createSpikeGeneratorGroup(str(self.label), self.shape, self.celltype.type)
        
        elif isinstance(self.celltype, cells.IF_cond_exp_gsfa_grr):
            self.carlsim_group = simulator.state.network.createGroupLIF(str(self.label), self.shape, self.celltype.type)
            parms = self.celltype.parameter_space
            simulator.state.network.setNeuronParametersLIF(self.carlsim_group, parms['tau_m'], parms['tau_refrac'], parms['v_thresh'], parms['v_reset'], self.celltype.rMem)
        
        else:
            raise ValueError("Unsupported cell type!")

    def _set_initial_value_array(self, variable, initial_value):
        """
        Empty method to suppress setting initial value
        Carlsim does not need initial value setting (handled internally)
        :param variable:
        :param initial_value:
        :return:
        """
        pass

    def _get_view(self, selector, label=None):
        pass

    def _get_parameters(self, parameter_space):
        pass
    
    def _set_parameters(self, parameter_space):
        pass

class PopulationView(common.PopulationView):
    _assembly_class = Assembly
    _simulator = simulator
