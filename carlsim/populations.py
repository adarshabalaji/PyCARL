import numpy
from pyNN import common
from pyNN.standardmodels import StandardCellType, cells
from pyNN.parameters import ParameterSpace, simplify
from . import simulator
from .recording import Recorder
from carlsim import *

#synapse_type = ''

class Assembly(common.Assembly):
    __doc__ = common.Assembly.__doc__
    _simulator = simulator

class Population(common.Population):
    __doc__ = common.Population.__doc__
    _simulator = simulator
    _recorder_class = Recorder
    _assembly_class = Assembly

    def _create_cells(self):
        id_range = numpy.arange(simulator.state.id_counter,
                                simulator.state.id_counter + self.size)
        self.all_cells = numpy.array([simulator.ID(id) for id in id_range],
                                     dtype=simulator.ID)
        self._mask_local = numpy.ones((self.size,), bool)

        for id in self.all_cells:
            id.parent = self
        simulator.state.id_counter += self.size
       
	if isinstance(self.celltype, cells.SpikeSourceArray):
            self.carlsim_group = simulator.state.network.createSpikeGeneratorGroup(str(self.label), self.size, self.celltype.type)
            #self.celltype.parameter_space._set_shape((3,))
            #self.celltype.parameter_space.evaluate()
        
        if isinstance(self.celltype, cells.Izhikevich):
            self.carlsim_group = simulator.state.network.createGroup(str(self.label), self.size, self.celltype.type)
            #self.celltype.parameter_space._set_shape((self.size,))
            #self.celltype.parameter_space._set_shape((3,))
            #self.celltype.parameter_space.evaluate()
            parameters = self.celltype.parameter_space
            simulator.state.network.setNeuronParameters(self.carlsim_group, parameters['a'], parameters['b'],
                                                        parameters['c'], parameters['d'])

        self._simulator.state.groupIDs.append(self.carlsim_group)

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
