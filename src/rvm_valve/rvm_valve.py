#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This driver controls OEM AVM rotary valves from Advanced Microfluidics.
https://github.com/tnaegele/rvm_valve

@author: Tobias E. Naegele, 02/2024

Copyright (c) 2024 Tobias E. Naegele

'''

__author__ = "Tobias E. Naegele"
__maintainer__ = __author__
__version__ = "1.0"
__email__ = "github@tobiasnaegele.com"

import serial
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')


class rvm_valve():
    '''
    This driver controls OEM AVM rotary valves from Advanced Microfluidics.
    '''
    def __init__(self, port, number_of_ports=12):
        '''
        Initialise valve control

        Parameters
        ----------
        port : str
            Port of valve, e.g. 'COM2' on Windows or device path of Linux / MacOS
            
        number_of_ports : int, optional
            Number of valve ports. The default is 12.

        Returns
        -------
        None.

        '''
        self.valve = serial.Serial(port, 9600, timeout=1000)
        logging.info(f'connected to RVM valve {self.valve.name}')
        self.number_of_ports = number_of_ports
        self.current_valve_position = 1  # keeps track of the valve position
        self.home()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        '''
        Closes connection to valve.

        Returns
        -------
        int
            0 if executed successfully.

        '''
        self.valve.close()
        logging.info('MUX connection closed')
        return 0

    def _execute(self, command):
        '''
        Send command to valve.

        Parameters
        ----------
        command : str
            Command as outlined in manual.

        Returns
        -------
        int
            0 if executed successfully.

        '''
        command_string = str.encode(
            '/1' + command + '\r')  # add prefix and suffix and convert to bytes
        logging.info(f'MUX write {command_string}')
        self.valve.write(command_string)
        reply = self._serial_read()  # read reply from valve
        self._handle_reply(reply)
        return 0

    def _serial_read(self):
        '''
        Reads replies from valve

        Returns
        -------
        reply : str
            Reply from valve.

        '''
        reply = self.valve.read(self.valve.inWaiting())
        return reply

    def _handle_reply(self, reply):
        ''' interprets reply from valve
            work in progress, currently just prints reply'''
        logging.info(f'MUX has replied {reply}')

    def home(self):
        '''
        Homes the valve

        Returns
        -------
        int
            0 if executed successfully.

        '''
        self.execute('ZR')
        self.current_valve_position = 1  # update valve position
        return 0

    def abort(self):
        '''
        aborts movement (?)
        command is not properly documented in mnaual so might not be functional

        Returns
        -------
        int
            0 if executed successfully.

        '''
        self.execute('T')
        return 0

    def move(self, new_channel, direction=0):
        '''
        Move valve to channel if not already at desired position

        Parameters
        ----------
        channel : int
            Desired channel position.
        
        direction : int, optional
            0: shortest path,  1: incrememtal, 2: decremental. The default is 0.

        Returns
        -------
        int
            New valve position. -1 if attempted to move valve beyond number of available ports

        '''
        if int(new_channel) not in range(1,self.number_of_ports+1):
            logging.warning(f'asked MUX to move to position {
                            new_channel} which does not exist')
            return -1

        new_channel = str(int(new_channel))
        direction = str(int(direction))

        if direction == '0':
            self.execute('b' + new_channel + 'R')
        elif direction == '1':
            self.execute('i' + new_channel + 'R')
        elif direction == '2':
            self.execute('o' + new_channel + 'R')

        self.current_valve_position = int(
            new_channel)  # update valve position
        return int(new_channel)

    def get_valve_postion(self):
        '''
        Reads the current valve position.
        Work in progress, needs proper way to handle response, currently does nothing.

        Returns
        -------
        int
            0 if executed successfully.

        '''
        self.execute('?6')
        return 0

