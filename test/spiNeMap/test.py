from numpy import arange
from pyNN.utility import get_simulator
import time
# Configure the application (i.e) configure the additional
# simualator parameters


sim, options = get_simulator(("netName", "String for name of simulation"),("--gpuMode", "Enable GPU_MODE (CPU_MODE by default)", {"action":"store_true"}), ("logMode", "Enter logger mode (USER by default)", {"default":"USER"}), ("ithGPUs", "Number of GPUs"), ("randSeed", "Random seed"))

##################################################################
# Utility section (move to different utility class later)
##################################################################
# Create file scope vars for options
netName = None
simMode = None

logMode = None
ithGPUs = None
randSeed = None

# Validate and assign appropriate options
netName = options.netName

if options.gpuMode:
    simMode = sim.GPU_MODE
else:
    simMode = sim.CPU_MODE

if options.logMode == "USER":
    logMode = sim.USER
elif options.logMode == "DEVELOPER":
    logMode = sim.DEVELOPER

ithGPUs = int(options.ithGPUs)

if (simMode == sim.CPU_MODE and int(ithGPUs) > 0 ):
    print("Simulation set to CPU_MODE - overriding numGPUs to 0")

ithGPUs = 0

randSeed = int(options.randSeed)

##################################################################
# Start of application code
##################################################################
sim.setup(timestep=0.01, min_delay=1.0, netName = netName, simMode = simMode, logMode = logMode, ithGPUs = ithGPUs, randSeed = randSeed)
spike_source = sim.Population(1,sim.SpikeSourceArray("test",1,"excitatory", "COBA"))
neurons = sim.Population(3, sim.Izhikevich(a=0.02, b=0.2, c=-65, d=6, i_offset=[0.014, 0.0, 0.0]))
connection = sim.Projection(spike_source, neurons, sim.OneToOneConnector(),receptor_type='excitatory')

sim.state.setupNetwork()
print("Reached Here")
sim.run(100, callbacks=[])

#sim.state.end()
