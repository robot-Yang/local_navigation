/*
计算点云重心

 点云的重心是一个点坐标，计算出云中所有点的平均值。
你可以说它是“质量中心”，它对于某些算法有多种用途。
如果你想计算一个聚集的物体的实际重心，
记住，传感器没有检索到从相机中相反的一面，
就像被前面板遮挡的背面，或者里面的。
只有面对相机表面的一部分。

*/
#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>

#include <pcl/common/centroid.h>
#include <iostream>
#include <vector>

ros::Publisher pub;

void
cloud_cb (const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
{

  // Container for original & filtered data
  pcl::PCLPointCloud2* cloud = new pcl::PCLPointCloud2; 
  pcl::PCLPointCloud2 cloud_filtered;

  // Convert to PCL data type
  pcl_conversions::toPCL(*cloud_msg, *cloud);

  // conversion
  pcl::PointCloud<pcl::PointXYZ> point_cloud;
  pcl::PointCloud<pcl::PointXYZ>::Ptr point_cloudPtr(new pcl::PointCloud<pcl::PointXYZ>);
  pcl::fromPCLPointCloud2( *cloud, point_cloud);
  pcl::copyPointCloud(point_cloud, *point_cloudPtr);

  // 创建存储点云重心的对象
  Eigen::Vector4f centroid0;//齐次表示 
  pcl::compute3DCentroid(*point_cloudPtr, centroid0);
  std::cout << "The XYZ coordinates of the centroid are: ("
            << centroid0[0] << ", "
            << centroid0[1] << ", "
            << centroid0[2] << ")." << std::endl;

   pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cet_ptr(new pcl::PointCloud<pcl::PointXYZ>);
 //随机创建点云并打印出来
   cloud_cet_ptr->width  = 1;
   cloud_cet_ptr->height = 1;
   cloud_cet_ptr->points.resize (cloud_cet_ptr->width * cloud_cet_ptr->height);

   for (size_t i = 0; i < cloud_cet_ptr->points.size (); ++i)
   {
    cloud_cet_ptr->points[i].x = centroid0[0];
    cloud_cet_ptr->points[i].y = centroid0[1];
    cloud_cet_ptr->points[i].z = centroid0[2];
   }

  cloud_cet_ptr->header.frame_id = point_cloudPtr->header.frame_id;
  pcl::toPCLPointCloud2(*cloud_cet_ptr, cloud_filtered);
  sensor_msgs::PointCloud2 centroid;
  pcl_conversions::fromPCL(cloud_filtered, centroid);

  // Publish the data
  pub.publish (centroid);

}

int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "centroid_back");
  ros::NodeHandle nh;

  ros::Subscriber sub2 = nh.subscribe ("/chair_back", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
  pub = nh.advertise<sensor_msgs::PointCloud2> ("centroid_back", 1);

  // Spin
  ros::spin ();
}
