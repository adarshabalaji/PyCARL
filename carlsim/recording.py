import numpy
from pyNN import recording
from pyNN.carlsim import simulator

class Recorder(recording.Recorder): 
    _simulator = simulator
    
    def __init__(self, population, file=None):
        super(Recorder, self).__init__(population, file=file)
        self.event_output_files = []    
        self.displays = []
        self.output_files = []

    def _record(self, variable, new_ids, sampling_interval=None):                                                                                                                                                                     
        #for id in new_ids:
        if variable == 'spikes':
           simulator.state.network.setSpikeMonitor(self.population.carlsim_group, "DEFAULT")
