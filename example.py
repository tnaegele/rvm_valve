#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example for rvm_valve package on https://github.com/tnaegele/rvm_valve

@author: Tobias E. Naegele, 02/2024

Copyright (c) 2024 Tobias E. Naegele
"""
import rvm_valve
import time

with rvm_valve.rvm_valve('COM7') as valve:
    time.sleep(3)
    valve.home()
    time.sleep(3)
    valve.move(5)
    time.sleep(3)
    valve.move(4,direction=1)
