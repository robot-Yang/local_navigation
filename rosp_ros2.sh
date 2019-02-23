source /opt/ros/kinetic/setup.bash
echo 'source /opt/ros/kinetic/setup.bash' >> ~/.bashrc
mkdir -p ~/catkin_workspace/src
cd catkin_workspace/src
catkin_init_workspace
cd ~/catkin_workspace/
catkin_make
source ~/catkin_workspace/devel/setup.bash
echo 'source ~/catkin_workspace/devel/setup.bash' >> ~/.bashrc
export | grep ROS
