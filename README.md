# PyCARL
Files to interface CARLsim to the pyNN framework.

# Command to run test.py with the CARLsim engine
python test.py carlsim "test" USER 1 42


# Carlsim Folder
1. /carlsim folder contains the python files required to interface pyNN to CARLsim4.
2. The contents of /carlsim are generated using the contents in the source folder. 
 


# Source Folder
1. Follow the steps below to compile a new pyNN interface (carlsim.i and carlsim_wrap.cxx) with the static library libcarsim.a (generated during a
   CARLsim build). (command also in the notes folder)


#####################################################################################  

# Installation 

##################################################################################### 

# 1. Installing PyNN:  
```
$ pip install pyNN 
```
Or follow the instructions in  

http://neuralensemble.org/docs/PyNN/installation.html 



###################################################################################### 



# 2. Compile and install PyCARL  

2.1 Clone the PyCARL repository to the CARLsim root.  
```
$ cd CARLsim4/ 

$ git clone https://github.com/adarshabalaji/PyCarlsim.git 
```
  


2.2 Compile and generate the pyNN -> carlsim  interface file (carlsim.py) 

# 2.2.1 Install SWIG:  
```
$ sudo apt update 

$ sudo apt install swig 
```
 

2.2.2 Compile and link the interface file (carlsim_wrap.cxx), generated by swig, with the libcarlsim.a library.  
```
$ cd source  

$ source build.sh 
```
This creates a static library _carlsim.so and a pyNN -> CARLsim interface (carlsim.py) 

 
# 3. Copy the compiled sources and the carlsim/ folder in the pyCARL repo to pyNN.  
```
$ cp –r CARLsim4/pyCARL/carlsim <root of pyNN Installation>  
```
3.1 Copy the generated _carlsim.so and carlsim.py file to root-of-pyNN-Installation/carlsim 

 
PyCARL is now integrated with pyNN.  
 



###################################################################################### 

# **OPTIONAL** If you want to compile and link the interface file manually, then   


4.1 Compile the carlsim.i (interface file) using SWIG 
```
$ cd source 

$ swig -c++ -python carlsim.i 
```
The output of the swig build is a wrapper file (carlsim_wrap.cxx) and the pyNN -> carlsim interface file (carlsim.py). 

 

4.2 In the source folder, follow the steps below to compile a new pyNN interface (carlsim.i and carlsim_wrap.cxx) with the static library libcarsim.a (generated during a CARLsim build).  
```
$gcc -fPIC -c carlsim_wrap.cxx -I/usr/include/python<version> -I<CARLsim4 include dir> -I/usr/local/cuda/include -I/usr/local/cuda/samples/common/inc -D__NO_CUDA__ 
```
Update the above command with the python version of choice and the CARLsim4 installation directory. 

4.3 Link the carlsim_wrap.o file to the libcarlsim.a file.  
```
$ g++ -shared carlsim_wrap.o -o _carlsim.so 

$ g++ -shared ~/CARL/lib/libcarlsim.a carlsim_wrap.o -o _carlsim.so 
```
  
###################################################################################### 


