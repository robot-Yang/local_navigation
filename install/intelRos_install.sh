mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src/
wget https://github.com/intel-ros/realsense/archive/2.2.17.tar.gz
tar zxvf 2.2.17.tar.gz

catkin_init_workspace 
cd ..
catkin_make clean
catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
catkin_make install
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
