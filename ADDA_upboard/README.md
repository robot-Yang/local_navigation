# This folder contains python file for AD/DA board

# test.py is the same with the one for raspberry

# HighPrecision_ADDA.py is changed for upboard

1. line 5: 'import mraa'
the biggest change here is to replace RPi.GPIO with mraa library
the mraa github repository is here: https://github.com/intel-iot-devkit/mraa, including the installing command

2. line 17:
use 'self._spi.open(1, 0)' to replace 'self._spi.open(0, 0)' 

3. line 21~ 31, line 108~ 124, line 203: 
use the mraa responding output, input, pull_up fucntion to replace RPi.GPIO's

# enable spi in userspace  
https://wiki.up-community.org/Pinout_UP2#SPI_Ports