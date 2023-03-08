#!/usr/bin/env python

import numpy as np
import pyfirmata
import time
import pandas as pd
from pandas import DataFrame

# Initialize hardware parameters
board = pyfirmata.Arduino("COM3")
readMuxS2 = board.get_pin('d:2:o')
readMuxS1 = board.get_pin('d:3:o')
readMuxS0 = board.get_pin('d:4:o')   # MUX that reads copper tape voltage
writeMuxS2 = board.get_pin('d:5:o')
writeMuxS1 = board.get_pin('d:6:o')
writeMuxS0 = board.get_pin('d:7:o')  # MUX that turns on copper tapes
priMuxS2 = board.get_pin('d:8:o')
priMuxS1 = board.get_pin('d:9:o')
priMuxS0 = board.get_pin('d:10:o')   # Primary MUX that controls other MUX
input0 = board.get_pin('a:0:i')
input1 = board.get_pin('a:1:i')
input2 = board.get_pin('a:2:i')
input3 = board.get_pin('a:3:i')    # Input channels on Arduino

# Declare some useful variables
data0 = np.empty([1,8])
data1 = np.empty([1,8])
data2 = np.empty([1,8])
data3 = np.empty([1,8])
dataAll = np.zeros([32, 32])

# Check if the input is a valid number
def isNaN(num):
    return num != num

# Select channel using given pin number
def selectChannel(channel, S2, S1, S0):
    # print("Selecting channel %s"%channel)

    # turn off all pins
    S2.write(0)
    S1.write(0)
    S0.write(0)

    # turn on corresponding pins
    if (channel >= 4):
        S2.write(1)
        channel = channel - 4
    
    if (channel >= 2):
        S1.write(1)
        channel = channel - 2
    
    if (channel == 1):
        S0.write(1)

# Read row copper tape input
def readCu():
    # Use read MUX to select copper tapes
    for index in range(8):
        selectChannel(index, readMuxS2, readMuxS1, readMuxS0)
        # print("Reading row %s"%index)
        # Record reading from Arduino pins
        in0 = input0.read()
        while(in0 == None):     # Check if the first reading is corrupted
            in0 = input0.read()
            board.pass_time(0.001)
            print("Invalid reading discarded.")
        data0[0][index] = in0
        data1[0][index] = input1.read()
        data2[0][index] = input2.read()
        data3[0][index] = input3.read()
        board.pass_time(0.01)

# Turn on column copper tape one by one
def writeCu():
    # Use primary MUX to select secondary MUX
    for i in range(1):
        # print("Setting secondary MUX")
        selectChannel(i, priMuxS2, priMuxS1, priMuxS0)
        # print("Secondary MUX %s selected"%i)
        # Use secondary MUX to select copper tapes
        for j in range(8):
            # print("Setting copper tapes %s"%j)
            selectChannel(j, writeMuxS2, writeMuxS1, writeMuxS0)
            readCu()
            dataTemp = np.vstack((data0.T, data1.T, data2.T, data3.T))
            dataAll[:,i*8+j] = dataTemp[:,0]

def main():
    # Start serial communication
    it = pyfirmata.util.Iterator(board)
    it.start() 

    # Constantly recording the baseline values
    """ index = 10  # Read and print data for 10 cycles
    count = 0
    while count < index:
        writeCu()
        print(dataAll[0:20, 0:9])

        # Write to excel
        df = DataFrame(dataAll[0:20, 0:9])
        with pd.ExcelWriter('test.xlsx', engine='openpyxl', mode = 'a', if_sheet_exists = 'overlay') as writer:
            df.to_excel(writer, startrow = count*20, index = False, header = False)
        count = count + 1 """

    # Read values repetitively and take the average
    base_sum = np.zeros([32, 32])
    for index in range(20):
        writeCu()
        base_sum = base_sum + dataAll
        print("Read iteration #%s completed"%str(index+1))
        df = DataFrame(dataAll[0:24, 0:8])
        with pd.ExcelWriter('record.xlsx', engine='openpyxl', mode = 'a', if_sheet_exists = 'overlay') as writer:
            df.to_excel(writer, startrow = index*24, index = False, header = False)
    avg_sum = base_sum / 20
    df = DataFrame(dataAll)
    df.to_excel('square.xlsx', sheet_name='sheet1', index = False, header = False)

if __name__ == "__main__":
    main()    



