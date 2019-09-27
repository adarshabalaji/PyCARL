from carlsim import *
import logging
from pyNN import common
from pyNN.common.control import DEFAULT_MAX_DELAY, DEFAULT_TIMESTEP, DEFAULT_MIN_DELAY

name = "carlsim"
logger = logging.getLogger("PyNN")

class ID(int, common.IDMixin):

    def __init__(self, n):
        """Create an ID object with numerical value `n`."""
        int.__init__(n)
        common.IDMixin.__init__(self)

class State(common.control.BaseState):

	def __init__(self):
		self.initsuccess = False
		common.control.BaseState.__init__(self)
		self.network 		= None
		self.netName 		= None
		self.simMode 		= None
		self.logMode 		= None
		self.ithGPUs 		= None
		self.randSeed 		= None
		self.clear()

	def set_params_and_init(self, extra_params):
		for key in extra_params:
			if key == "netName":
				self.netName = extra_params[key]
			elif key == "simMode":
				self.simMode = extra_params[key]
			elif key == "logMode":
				self.logMode = extra_params[key]
			elif key == "ithGPUs":
				self.ithGPUs = extra_params[key]
			elif key == "randSeed":
				self.randSeed = extra_params[key]
		
		self.network = CARLsim(self.netName, self.simMode, 
								self.logMode, self.ithGPUs,
								self.randSeed)
		
		self.initsuccess = True

	def clear(self):
		self.id_counter = 0

	def reset(self):
		pass

############################################################################
# Params to suppress recording errors - not used otherwise
############################################################################
	dt = DEFAULT_TIMESTEP
	@property
	def t(self):
		return 0
############################################################################
state = State()
