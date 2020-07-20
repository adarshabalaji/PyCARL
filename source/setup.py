#!/usr/bin/env python

"""
setup.py file 
"""

from distutils.core import setup, Extension


carlsim_module = Extension('_carlsim',
                           sources=['carlsim_wrap.cxx', '../../CARLsim4/carlsim/interface/src/carlsim.cpp',
                           '../../CARLsim4/carlsim/interface/src/callback_core.cpp', 
                           '../../CARLsim4/carlsim/interface/src/linear_algebra.cpp', 
                           '../../CARLsim4/carlsim/interface/src/poisson_rate.cpp', 
                           '../../CARLsim4/carlsim/interface/src/user_errors.cpp',
                           '../../CARLsim4/carlsim/kernel/src/print_snn_info.cpp',
                           '../../CARLsim4/carlsim/kernel/src/snn_cpu_module.cpp',
                           '../../CARLsim4/carlsim/kernel/src/snn_manager.cpp',
                           '../../CARLsim4/carlsim/kernel/src/spike_buffer.cpp',
                           '../../CARLsim4/carlsim/monitor/connection_monitor.cpp',
                           '../../CARLsim4/carlsim/monitor/connection_monitor_core.cpp',
                           '../../CARLsim4/carlsim/monitor/group_monitor.cpp',
                           '../../CARLsim4/carlsim/monitor/group_monitor_core.cpp',
                           '../../CARLsim4/carlsim/monitor/spike_monitor.cpp',
                           '../../CARLsim4/carlsim/monitor/spike_monitor_core.cpp',
                           '../../CARLsim4/carlsim/monitor/neuron_monitor.cpp',
                           '../../CARLsim4/carlsim/monitor/neuron_monitor_core.cpp',
                           '../../CARLsim4/tools/spike_generators/spikegen_from_vector.cpp',
                           '../../CARLsim4/tools/visual_stimulus/visual_stimulus.cpp'
                           ]
                           )


setup (name = 'carlsim',
       version = '0.2',
       description = """CARLsim simulator as Python library""",
       ext_modules = [carlsim_module],
       py_modules = ["carlsim"],
       )
