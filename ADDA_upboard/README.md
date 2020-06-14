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

# install pip  
sudo apt install python-pip

# install spidev  
pip install spidev
  #Alternative if problems with pip
sudo python -m pip install spidev 

# add missing firmware from  
https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/i915

# enablel spi port on UP board  
https://wiki.up-community.org/Pinout_UP2#SPI_Ports

# Enable the HAT functionality from userspace  
https://wiki.up-community.org/Ubuntu

# error shooting  
1. if there is an error related to 'time out', remember to check if the time zone is right or not.  
2. error: invalid GPIO or something, please check if you already replaced the kernel with the one provided by upboard.
checking method: enter 'uname -a' into command line, if already replaced, the print out should be similar to 'Linux upsquared-UP-APL01 4.15.0-37-generic #40~upboard03-Ubuntu SMP Wed Dec 12 16:21:24 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux', '#40~upboard03-Ubuntu' means this kernel is from upboard.
if not replace yet, please follow the tutorial here:
https://wiki.up-community.org/Ubuntu  
3. if the readings from sensor is very unstable(ex: 2888888) especially for the upper ADDA board, this is causded by the ADC pins are all exposed to the air.
