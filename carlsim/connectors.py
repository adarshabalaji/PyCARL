"""
Connection method classes for the neuron module

:copyright: Copyright 2006-2016 by the PyNN team, see AUTHORS.
:license: CeCILL, see LICENSE for details.

"""
import pyNN.carlsim.carlsim

from pyNN.connectors import AllToAllConnector, \
                            OneToOneConnector, \
                            FixedProbabilityConnector, \
                            DistanceDependentProbabilityConnector, \
                            DisplacementDependentProbabilityConnector, \
                            IndexBasedProbabilityConnector, \
                            FromListConnector, \
                            FromFileConnector, \
                            FixedNumberPreConnector, \
                            FixedNumberPostConnector, \
                            SmallWorldConnector, \
                            CSAConnector, \
                            CloneConnector, \
                            ArrayConnector, \
                            FixedTotalNumberConnector



class AllToAllConnector(AllToAllConnector):
    pass

class GaussianConnector():
    pass 
