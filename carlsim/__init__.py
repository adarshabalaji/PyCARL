"""
CARLsim implementation of the PyNN API.

:copyright: Copyright 2006-2100 Prathyusha Adiraju
:license: Mushti license DO NOT BREACH
"""

from carlsim import *
from . import simulator
from .standardmodels.cells import *
from pyNN.connectors import *
from .standardmodels.synapses import *
from .projections import Projection
from .populations import Population
from pyNN import common
from pyNN.common.control import DEFAULT_MAX_DELAY, DEFAULT_TIMESTEP, DEFAULT_MIN_DELAY


def setup(timestep=DEFAULT_TIMESTEP, min_delay=DEFAULT_MIN_DELAY,
           **extra_params):
	common.setup(timestep, min_delay, **extra_params)
	simulator.state.set_params_and_init(extra_params)
	

