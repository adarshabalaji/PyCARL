#!/usr/bin/env sh

CARLSIM4_INSTALL_DIR=$(HOME)/CARL

swig -c++ -python carlsim.i
mkdir -p bin/
mv carlsim.py bin/

# TO BUILD FOR PYTHON2
python2 setup.py build_ext -b ./bin/ -t ./bin/wrap --warnings --define __NO_CUDA__ --include /home/adarsha/CARL/include:/usr/local/cuda/include:/usr/local/cuda/samples/common/inc

# TO BUILD FOR PYTHON3
# swig -c++ -python -py3 carlsim.i
# python3 setup.py build_ext --inplace --define __NO_CUDA__ --include ../carlsim/kernel/inc/:../carlsim/monitor/:../carlsim/interface/inc/:../tools/spike_generators/

# TO BUILD FOR CUDA SUPPORT
# TODO: Figure out what needs including to fix errors
# python2 setup.py build_ext --inplace --define __CUDA9__ --include ../carlsim/kernel/inc/:../carlsim/monitor/:../carlsim/interface/inc/:../tools/spike_generators/:/usr/local/cuda/include/:/usr/local/cuda/samples/common/inc
