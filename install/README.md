# local_navigation

1. Ubuntu installation && Install Ubuntu kernel 4.15.0 for UP from PPA  
https://wiki.up-community.org/Ubuntu  
Commands in: up2_change.sh  
*Do not upgrade to ubuntu 18  
*choose "NO" for the question: "abort kernal removal"

2. Install Intel® RealSense™ SDK 2.0 from Debian Package  
https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md#installing-the-packages  
Commands in: realsense_install.sh  
*run: realsense-viewer to verify the installation.

3.  Install the ROS distribution  
http://wiki.ros.org/kinetic/Installation/Ubuntu  
Commands in: ros_install.sh  
*Before running the command, configure your Ubuntu repositories to allow "restricted," "universe," and "multiverse." and choose a better server: like tsukuba…

4.  Install Intel® RealSense™ ROS from Sources  
https://github.com/intel-ros/realsense  
Commands in: intelRos_install.sh  
*Pay attention to choosing a suitable mirror(related to the download speed)

5. PCL installation  
(1). form binary package  
  sudo add-apt-repository ppa:v-launchpad-jochen-sprickerhof-de/pcl  
  sudo apt-get update  
  sudo apt-get install libpcl1  
(2). from Source  
  Commands in: pcl_install.sh

6. Install ROS in Raspberry Pi  
https://github.com/ROSbots/rosbots_setup_tools#use-our-existing-rosbots-raspbianrosopencv-image-after-youve-downloaded-it

7. Set up connection between Raspberry Pi and UP Square  
https://www.intorobotics.com/how-to-setup-ros-kinetic-to-communicate-between-raspberry-pi-3-and-a-remote-linux-pc/


Problems shot:  
1. No rule to make target '/usr/lib/x86_64-linux-gnu/libvtkproj4-6.2.so.6.2.0'  
-> sudo apt-get install libvtk6-dev libvtk6.2 libvtk6.2-qt
