
import time

t= time.time()
from numpy import arange
from pyNN.utility import get_simulator
from pyNN.carlsim import *
importTime = time.time() - t
# Configure the application (i.e) configure the additional
# simualator parameters


t= time.time()
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

#stim = VisualStimulus("temp.dat")
#length = int(stim.getLength()) 

#imgDim = Grid3D(stim.getWidth(), stim.getHeight(), 1) 
#imgSmallDim = Grid3D(stim.getWidth()/2, stim.getHeight()/2, 1) 
imgDim = 784
imSmallDim = 196

##################################################################
# Define the neuron groups.
##################################################################

# create a spike generator group.
inputCellType = sim.SpikeSourceArray("input", 784, "EXCITATORY_NEURON", "CUBA")
spike_source = sim.Population(784, inputCellType, label='input')

# create neuron groups. 
izhikevichCellType1 = sim.Izhikevich("EXCITATORY_NEURON", a=0.02, b=0.2, c=-65, d=8, i_offset=[0.014, 0.0, 0.0])
gSmoothExc = sim.Population(196, izhikevichCellType1, label='smoothExc')

# create neuron groups. 
izhikevichCellType2 = sim.Izhikevich("INHIBITORY_NEURON", a=0.02, b=0.2, c=-65, d=8, i_offset=[0.014, 0.0, 0.0])
gSmoothInh = sim.Population(196, izhikevichCellType2, label='smoothInh')

# create neuron groups. 
gEdges = sim.Population(196, izhikevichCellType1, label='edges')

##################################################################
# Define the connections.
##################################################################

# connect input to exc - "gaussian"
#connection = sim.Projection(spike_source, neuron_group1, sim.AllToAllConnector(), receptor_type='excitatory')
connection = sim.state.network.connect(0, 1, "gaussian", RangeWeight(int(70)), 1,  RangeDelay(1), RadiusRF(float(0.5), float(0.5),-1))

# connect the input to the inhibitory neuron
connection2 = sim.state.network.connect(0, 2, "gaussian", RangeWeight(int(2)), 1,  RangeDelay(1), RadiusRF(float(3), float(3),-1))


connection3 = sim.Projection(gSmoothExc, gEdges, sim.OneToOneConnector(), receptor_type='excitatory')


connection4 = sim.Projection(gSmoothInh, gEdges, sim.OneToOneConnector(), receptor_type='excitatory')

##################################################################
# Setup Network (function native to CARLsim) 
# Record functions can only be called after the setupNetwork 
# function is called.
##################################################################

sim.state.network.setupNetwork()

spike_source.record('spikes')
gSmoothExc.record('spikes')
gSmoothInh.record('spikes')
gEdges.record('spikes')

P = PoissonRate(int(784), bool(0))
P.setRates(5)
sim.state.network.setSpikeRate(0, P)

sim.run(1000)
runTime = time.time()  - t

print(runTime)
print(importTime)
#sim.state.network.runNetwork(1, 0, True)
#sim.state.end()
