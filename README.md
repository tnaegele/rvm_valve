# rvm_valve_control
Python driver for the [Advanced Microfluidics OEM AVM rotary valve](https://amf.ch/product/rvm-microfluidic-electric-rotary-valve/). This driver *might* also work with the [Elveflow microfluidic distribution valve (MUX)](https://www.elveflow.com/microfluidic-products/microfluidics-flow-control-systems/mux-distrib/) which internally uses the same hardware.

## Usage
Just clone this repo and create a virtualenv which fulfils the requirements from requirements.txt. 

API documentation can be found at: https://tnaegele.github.io/rvm_valve

Example code:
~~~python
import rvm_valve
import time

with rvm_valve.rvm_valve('COM7') as valve:
    time.sleep(3)
    valve.home()
    time.sleep(3)
    valve.move(5)
    time.sleep(3)
    valve.move(4,direction=1)
~~~

## Todo
- add proper handling of responses from valve with method `_handle_reply()`
- make `get_valve_position()` method functional
- test whether the driver works with Elveflows MUX
- write port autodetection function

## Useful links
- rotary valve manual: https://amf.ch/app/uploads/2023/09/AMF-RVM-Electric-Rotary-Valve-Operating-Manual.pdf
