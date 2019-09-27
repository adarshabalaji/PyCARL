import numpy
from pyNN import recording
from pyNN.carlsim import simulator

class Recorder(recording.Recorder):
    """Encapsulates data and functions related to recording model variables."""
    _simulator = simulator
    # scale_factors = {'spikes': 1,
    #                  'v': 1,
    #                  'w': 0.001,
    #                  'gsyn': 0.001}  # units conversion

    def __init__(self, population, file=None):
        __doc__ = recording.Recorder.__doc__
        recording.Recorder.__init__(self, population, file)