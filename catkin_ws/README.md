# catkin_ws

This is a ROS directionary, all codes in src folder.
1. realsense-2.2.0 is an Intel® RealSense™ ROS from Sources folder, you could update it as you want.  
The link is here: https://github.com/intel-ros/realsense

2. ros_seg is to set up a node to view all the segmented parts in dfferent colors.

3. cluster_show_chair is to get the chair's pointcloud only.

4. region_growing_segmentation is to seperate the chair's bottom and back.

5. centroid_bottom is to get the centroid of chair's bottom.

6. centroid_back is to get the centroid of chair's back.

All folder could establish nodes to listen to the messages published by the previous step and publish new messages.

Compile all codes (Commands in intelRos_install.sh or https://github.com/intel-ros/realsense)  

Run 
```
roslaunch realsense2_camera demo_pointcloud.launch
```
to get the original pointcloud and visualize it in rviz 

Run 
```
roslaunch realsense2_camera dock_centroid.launch
```
to deal with pointcloud  

Configuration of rviz is stored in rviz_config folder as config1.rviz
