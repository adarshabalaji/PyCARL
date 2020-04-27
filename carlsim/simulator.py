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
		self.id_counter         = 0
                self.num_processes      = 1
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

	def run(self, simtime):
            #simtime in PyNN is provided in milliseconds
            nSec = simtime/1000
            nMsec = simtime%1000
            self.network.runNetwork(int(nSec), int(nMsec))	

	def run_until(self, tstop):
	    # get the present sim time compute the time to run until
            time = int(self.network.getSimTimeMsec())
            runtime=0
            if tstop > time:
                runtime = tstop - time

            nSec = runtime/1000
            nMsec = runtime%1000
            self.network.runNetwork(int(nSec), int(nMsec))	
	
        def setupNetwork(self):
            self.network.setupNetwork()

        def clear(self):
	    pass	
		
	# cannot be implemented with CARLsim
        def reset(self):
	    pass	

        def _get_dt(self):
	    pass	

	def _set_dt(self, timestep):
	    pass	

	def _get_min_delay(self):
	    pass
	
	def _set_min_delay(self, delay):
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
