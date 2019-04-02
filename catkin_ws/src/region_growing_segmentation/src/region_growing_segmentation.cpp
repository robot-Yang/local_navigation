#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>

#include <iostream>
#include <vector>
#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/features/normal_3d.h>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/filters/passthrough.h>
#include <pcl/segmentation/region_growing.h>

ros::Publisher pub1;
ros::Publisher pub2;

void
cloud_cb (const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
{
  // Container for original & filtered data
  pcl::PCLPointCloud2* cloud = new pcl::PCLPointCloud2; 
  pcl::PCLPointCloud2ConstPtr cloudPtr(cloud);
  pcl::PCLPointCloud2 cloud_filtered;

  // Convert to PCL data type
  pcl_conversions::toPCL(*cloud_msg, *cloud);

  // conversion
  pcl::PointCloud<pcl::PointXYZ> point_cloud;
  pcl::PointCloud<pcl::PointXYZ>::Ptr point_cloudPtr(new pcl::PointCloud<pcl::PointXYZ>);
  pcl::fromPCLPointCloud2( *cloud, point_cloud);
  pcl::copyPointCloud(point_cloud, *point_cloudPtr);

  pcl::search::Search<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
  pcl::PointCloud <pcl::Normal>::Ptr normals (new pcl::PointCloud <pcl::Normal>);
  pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> normal_estimator;
  normal_estimator.setSearchMethod (tree);
  normal_estimator.setInputCloud (point_cloudPtr);
  normal_estimator.setKSearch (50);
  normal_estimator.compute (*normals);

  pcl::IndicesPtr indices (new std::vector <int>);
  pcl::PassThrough<pcl::PointXYZ> pass;
  pass.setInputCloud (point_cloudPtr);
  pass.setFilterFieldName ("z");
  pass.setFilterLimits (0.0, 2.0);
  pass.filter (*indices);

  pcl::RegionGrowing<pcl::PointXYZ, pcl::Normal> reg;
  reg.setMinClusterSize (10);
  reg.setMaxClusterSize (1000000);
  reg.setSearchMethod (tree);
  reg.setNumberOfNeighbours (50);
  reg.setInputCloud (point_cloudPtr);
  reg.setInputNormals (normals);
  reg.setSmoothnessThreshold (6.0 / 180.0 * M_PI);
  reg.setCurvatureThreshold (1.0);

  std::vector <pcl::PointIndices> clusters;
  reg.extract (clusters);

  //cluster write
  pcl::PointCloud<pcl::PointXYZ>::Ptr pointcloud_left(new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pointcloud_part0(new pcl::PointCloud<pcl::PointXYZ>);
  int i= 0;
  for (std::vector<pcl::PointIndices>::const_iterator it = clusters.begin(); it != clusters.end(); ++it)
  {
	  pcl::PointCloud<pcl::PointXYZ>::Ptr cluster(new pcl::PointCloud<pcl::PointXYZ>);

	  for (std::vector<int>::const_iterator pit = it->indices.begin(); pit != it->indices.end(); ++pit)

	  cluster->points.push_back(point_cloudPtr->points[*pit]);
	  cluster->width = cluster->points.size();
	  cluster->height = 1;
	  cluster->is_dense = true;

	  if (i == 0)
	  {
	  *pointcloud_part0 = *cluster;
	  }
	  else
	  {
	  *pointcloud_left += *cluster;		  
	  }

  i++;

  }

  std::cout << "Number of clusters is equal to " << clusters.size () << std::endl;
  std::cout << "First cluster has " << clusters[0].indices.size () << " points." << endl;
  std::cout << std::endl;

  // Convert to ROS data type
  pointcloud_part0->header.frame_id = point_cloudPtr->header.frame_id;
  pcl::toPCLPointCloud2(*pointcloud_part0, cloud_filtered);
  sensor_msgs::PointCloud2 chair_bottom;
  pcl_conversions::fromPCL(cloud_filtered, chair_bottom);

  // Publish the data
  pub1.publish (chair_bottom);

  // Convert to ROS data type
  pointcloud_left->header.frame_id = point_cloudPtr->header.frame_id;
  pcl::toPCLPointCloud2(*pointcloud_left, cloud_filtered);
  sensor_msgs::PointCloud2 chair_back;
  pcl_conversions::fromPCL(cloud_filtered, chair_back);

  // Publish the data
  pub2.publish (chair_back);

}

int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "chair_separate");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe ("/chair", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
  pub1 = nh.advertise<sensor_msgs::PointCloud2> ("chair_bottom", 1);
  pub2 = nh.advertise<sensor_msgs::PointCloud2> ("chair_back", 1);

  // Spin
  ros::spin ();
}
