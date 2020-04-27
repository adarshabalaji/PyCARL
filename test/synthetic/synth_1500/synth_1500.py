
import time

t = time.time()
from numpy import arange
from pyNN.utility import get_simulator
from pyNN.carlsim import *

importTime = time.time() - t

# Configure the application (i.e) configure the additional
# simualator parameters


t = time.time()
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

numNeurons = 1 

nExc1 = 500
nExc2 = 500
nExc3 = 500

##################################################################
# Define the neuron groups.
##################################################################

# create a spike generator group.
inputCellType = sim.SpikeSourceArray("input", nExc1, "EXCITATORY_NEURON", "CUBA")
spike_source = sim.Population(nExc1, inputCellType, label='input')

# create neuron groups. 
izhikevichCellType1 = sim.Izhikevich("EXCITATORY_NEURON", a=0.02, b=0.2, c=-65, d=8, i_offset=[0.014, 0.0, 0.0])
neuron_group1 = sim.Population(nExc2, izhikevichCellType1, label='exc1')

# create neuron groups. 
izhikevichCellType2 = sim.Izhikevich("EXCITATORY_NEURON", a=0.02, b=0.2, c=-65, d=8, i_offset=[0.014, 0.0, 0.0])
neuron_group2 = sim.Population(nExc3, izhikevichCellType1, label='exc2')

##################################################################
# Define the connections.
##################################################################

# connect input to exc - "one-to-one"
connection = sim.Projection(spike_source, neuron_group1, sim.AllToAllConnector(), receptor_type='excitatory')

# connect input to exc - "random connector"
connection = sim.Projection(neuron_group1, neuron_group2, sim.AllToAllConnector(), receptor_type='excitatory')

##################################################################
# Setup Network (function native to CARLsim) 
# Record functions can only be called after the setupNetwork 
# function is called.
##################################################################

# function has to be called before any record function is called. 
sim.state.setupNetwork()

spike_source.record('spikes')
neuron_group1.record('spikes')
neuron_group2.record('spikes')

P = PoissonRate(nExc1, bool(0))
P.setRates(100)
sim.state.network.setSpikeRate(0, P)

# start the recording of the groups


# run the simulation for 100ms
sim.run(1000)
runTime = time.time() - t

print(importTime)
print(runTime)
# start the recording of the groups

