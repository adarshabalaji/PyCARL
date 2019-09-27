# PyCarlsim
Files to interface CARLsim to the pyNN framework.

# carlsim folder
1. /carlsim folder contains the python files required to interface pyNN to CARLsim4.
2. The contents of /carlsim are generated using the contents in the source folder. 
 


# source folder
1. Follow the steps below to compile a new pyNN interface (carlsim.i and carlsim_wrap.cxx) with the static library libcarsim.a (generated during a
   CARLsim build). (command also in the notes folder)


commands: 
# requires swig
1. swig -c++ -python carlsim.i
# update the python version used, carlsim intallation location. 
2. gcc -fPIC -c carlsim_wrap.cxx -I/usr/include/python<X.X> -I../carlsim -I../tools -I/usr/local/cuda/include -I/usr/local/cuda/samples/common/inc
3. g++ -shared carlsim_wrap.o -o _carlsim.so
4. g++ -shared ~/CARL/lib/libcarlsim.a carlsim_wrap.o -o _carlsim.so

python2 setup.py build_ext --inplace --include-dirs /usr/local/cuda/include:/usr/local/cuda/samples/common/inc --define __NO_CUDA__


# test folder 
1. The test folder contains two files test.py and imageSmoothing.py
2. Test scripts written in pyNN format to test the pyNN+CARLsim4 interface. 
