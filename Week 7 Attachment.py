import os
import time
import busio
import digitalio
import board
import matplotlib.pyplot as plt
import numpy as np
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Declare some useful variables
data0 = np.empty([1,8])
data1 = np.empty([1,8])
data2 = np.empty([1,8])
data3 = np.empty([1,8])
dataAll = np.zeros([32, 32])

# Start serial communication
spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D6)
mcp= MCP.MCP3008(spi, cs)
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)

# Configure all pins
# board.17 -> s2 of pri MUX
# board.27 -> s1
# board.22 -> s0
# board.13 -> s2 of sec MUX
# board.19 -> s1
# board.26 -> s0
# board.16 -> s2 of row MUX
# board.20 -> s1
# board.21 -> s0

readMuxS2 = digitalio.DigitalInOut(board.D16)
readMuxS1 = digitalio.DigitalInOut(board.D20)
readMuxS0 = digitalio.DigitalInOut(board.D21)   # MUX that reads copper tape voltage
writeMuxS2 = digitalio.DigitalInOut(board.D13)
writeMuxS1 = digitalio.DigitalInOut(board.D19)
writeMuxS0 = digitalio.DigitalInOut(board.D26)  # MUX that turns on copper tapes
priMuxS2 = digitalio.DigitalInOut(board.D17)
priMuxS1 = digitalio.DigitalInOut(board.D27)
priMuxS0 = digitalio.DigitalInOut(board.D22)   # Primary MUX that controls other MUX

readMuxS2.direction = digitalio.Direction.OUTPUT
readMuxS1.direction = digitalio.Direction.OUTPUT
readMuxS0.direction = digitalio.Direction.OUTPUT
writeMuxS2.direction = digitalio.Direction.OUTPUT
writeMuxS1.direction = digitalio.Direction.OUTPUT
writeMuxS0.direction = digitalio.Direction.OUTPUT
priMuxS2.direction = digitalio.Direction.OUTPUT
priMuxS1.direction = digitalio.Direction.OUTPUT
priMuxS0.direction = digitalio.Direction.OUTPUT

# Select channel using given pin number
def selectChannel(channel, S2, S1, S0):
    # print("Selecting channel %s"%channel)

    # turn off all pins
    S2.value = False
    S1.value = False
    S0.value = False

    # turn on corresponding pins
    if (channel >= 4):
        S2.value = True
        channel = channel - 4
    
    if (channel >= 2):
        S1.value = True
        channel = channel - 2
    
    if (channel == 1):
        S0.value = True

# Read row copper tape input
def readCu():   
    # Use read MUX to select copper tapes
    for index in range(8):
        selectChannel(index, readMuxS2, readMuxS1, readMuxS0)
        # print("Reading row %s"%index)
        # Record reading from ADC pins
        
#         if(index == 5):
#             data0[0][index] = -1
#             data1[0][index] = -1
#             data2[0][index] = -1
#             data3[0][index] = -1
#         else:
#             data0[0][index] = chan0.voltage
#             time.sleep(0.005)
#             data1[0][index] = chan1.voltage
#             time.sleep(0.005)
#             data2[0][index] = chan2.voltage
#             time.sleep(0.005)
#             data3[0][index] = -1   
        
        data0[0][index] = chan0.voltage
        time.sleep(0.001)
        data1[0][index] = chan1.voltage
        time.sleep(0.001)
        data2[0][index] = chan2.voltage
        time.sleep(0.001)
        data3[0][index] = -1
        print('ADC voltage Channel 0: ', str(chan0.voltage) + "V")
        print('ADC voltage Channel 1: ', str(chan1.voltage) + "V")
        print('ADC voltage Channel 2: ', str(chan2.voltage) + "V")

# Turn on column copper tape one by one
def writeCu():          
    # Use primary MUX to select secondary MUX
    for i in range(3):
        # print("Setting secondary MUX")
        selectChannel(i, priMuxS2, priMuxS1, priMuxS0)
        # print("Secondary MUX %s selected"%i)
        # Use secondary MUX to select copper tapes
        jindex = 7
        for j in range(8):
            # print("Setting copper tapes %s"%j)
            selectChannel(jindex, writeMuxS2, writeMuxS1, writeMuxS0)
            readCu()
            dataTemp = np.vstack((data0.T, data1.T, data2.T, data3.T))
            dataAll[:,i*8+j] = dataTemp[:,0]
            jindex -= 1

def main():

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
    for index in range(1):
        writeCu()
        base_sum = base_sum + dataAll
        print("Read iteration #%s completed"%str(index+1))
        # df = DataFrame(dataAll[0:24, 0:8])
        # with pd.ExcelWriter('record.xlsx', engine='openpyxl', mode = 'a', if_sheet_exists = 'overlay') as writer:
        #     df.to_excel(writer, startrow = index*24, index = False, header = False)
    avg_sum = base_sum / 1
    # print(avg_sum)
    
    # with open("baself35.txt", "w") as txt_file:
    with open("leftf35_ang.txt", "w") as txt_file:
        count = 7
        for i in range(8):
            for j in range(24):
                txt_file.write('%s,'%avg_sum[count][j])
            txt_file.write('\n')
            count -= 1
        
        count = 15
        for i in range(8):
            for j in range(24):
                txt_file.write('%s,'%avg_sum[count][j])
            txt_file.write('\n')
            count -= 1        
            
        count = 19
        for index in range(4):
            for j in range(24):
                txt_file.write('%s,'%avg_sum[count][j])
            txt_file.write('\n')
            print(count)
            count += 1
           
        for j in range(24):
            txt_file.write('%s,'%avg_sum[18][j])
        txt_file.write('\n')
            
        for j in range(24):
            txt_file.write('%s,'%avg_sum[23][j])
        txt_file.write('\n')
    
    # df = DataFrame(dataAll)
    # df.to_excel('square.xlsx', sheet_name='sheet1', index = False, header = False)

if __name__ == "__main__":
    main()    