#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/passthrough.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/conversions.h>
#include <pcl/io/pcd_io.h>
#include <pcl/common/centroid.h>
#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/segmentation/region_growing.h>
#include <algorithm>
#include <string>
#include <vector>

#include <iostream>
#include <pcl/features/normal_3d.h>

ros::Publisher pub;

void
cloud_cb (const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
{
  // Container for original & filtered data
  pcl::PCLPointCloud2* cloud = new pcl::PCLPointCloud2; 
  pcl::PCLPointCloud2ConstPtr cloudPtr(cloud);
  pcl::PCLPointCloud2 cloud_filtered;

  // Convert to PCL data type
  pcl_conversions::toPCL(*cloud_msg, *cloud);

  // Perform the actual filtering
  pcl::VoxelGrid<pcl::PCLPointCloud2> sor;
  sor.setInputCloud (cloudPtr);
  sor.setLeafSize (0.02, 0.02, 0.02);
  sor.filter (cloud_filtered);

  // conversion
  pcl::PointCloud<pcl::PointXYZ> point_cloud;
  pcl::PointCloud<pcl::PointXYZ>::Ptr point_cloudPtr(new pcl::PointCloud<pcl::PointXYZ>);
  pcl::fromPCLPointCloud2( cloud_filtered, point_cloud);
  pcl::copyPointCloud(point_cloud, *point_cloudPtr);

  //pcl::IndicesPtr indices (new std::vector <int>);
  pcl::PassThrough<pcl::PointXYZ> pass;
  pass.setInputCloud (point_cloudPtr);
  pass.setFilterFieldName ("y");
  pass.setFilterLimits (-0.25, 0.3);
  pass.filter (*point_cloudPtr);
  std::cout << "filter0." << std::endl;

  pcl::IndicesPtr indices1 (new std::vector <int>);
  pcl::PassThrough<pcl::PointXYZ> pass1;
  pass1.setInputCloud (point_cloudPtr);
  pass1.setFilterFieldName ("z");
  pass1.setFilterLimits (0.0, 2.0);
  pass1.filter (*point_cloudPtr);
  std::cout << "filter1" << std::endl;


  // Creating the KdTree object for the search method of the extraction
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>);
  tree->setInputCloud(point_cloudPtr);

  std::vector<pcl::PointIndices> cluster_indices;
  pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
  ec.setClusterTolerance(0.1); // 2cm
  ec.setMinClusterSize(100); //100
  ec.setMaxClusterSize(100000);
  ec.setSearchMethod(tree);
  ec.setInputCloud(point_cloudPtr);
  ec.extract(cluster_indices);
  std::cout << "step3" << std::endl;

  //pcl::PointCloud<pcl::PointXYZ>::Ptr pointcloud_segmented(new pcl::PointCloud<pcl::PointXYZ>);
  
  //std::vector<int> counter
  std::vector<float> counter_average_z;
  //std::unordered_map<std::string, pcl::PointCloud<pcl::PointXYZ>::Ptr> pointcloud_all;

  int i= 0;
  for (std::vector<pcl::PointIndices>::const_iterator it = cluster_indices.begin(); it != cluster_indices.end(); ++it)
  {
    pcl::PointCloud<pcl::PointXYZ>::Ptr cluster(new pcl::PointCloud<pcl::PointXYZ>);
    
    float cluster_z = 0;
    float average_z = 0;

    for (std::vector<int>::const_iterator pit = it->indices.begin(); pit != it->indices.end(); ++pit)
    {
      cluster->points.push_back(point_cloudPtr->points[*pit]);
      //cluster_z += point_cloudPtr->points[*pit].z;
    }

    cluster->width = cluster->points.size();
    cluster->height = 1;
    cluster->is_dense = true;

    if (cluster->points.size() <= 0)
      break;

    Eigen::Vector4f centroid0;//齐次表示 
    pcl::compute3DCentroid(*cluster, centroid0);

    //std::cout << "point cloud " << cluster->points.size() << " points" << std::endl;
    std::stringstream ss;
    ss << "index" << i << ".pcd";
    pcl::io::savePCDFile(ss.str(), *cluster);

    std::cout << "compare_z: cluster" << i << centroid0[2] << std::endl;
    counter_average_z.push_back(centroid0[2]);

    std::cout << "step4" << std::endl;

  i++;

  }

  std::string varname = "index0.pcd";
  if (counter_average_z.size() >= 1)
  {
    int position = 0;
    std::vector<float>::iterator smallest;

    smallest = std::min_element(std::begin(counter_average_z), std::end(counter_average_z));
    std::cout << "step5 smallest" << *smallest << std::endl;

    position = std::distance(std::begin(counter_average_z), smallest);
    std::cout << "smallest z" << *smallest << std::endl;
    std::cout << "position " << position << std::endl;
    std::string varname = "index" + std::to_string(position) + ".pcd";
    //*pointcloud_chair = *SET_NAME[position]
  }


  pcl::PointCloud<pcl::PointXYZ>::Ptr pointcloud_chair(new pcl::PointCloud<pcl::PointXYZ>);
  if ( pcl::io::loadPCDFile <pcl::PointXYZ> (varname, *pointcloud_chair) == -1)
  {
    std::cout << "Cloud reading failed." << std::endl;
  }

  // Convert to ROS data type
  pointcloud_chair->header.frame_id = point_cloudPtr->header.frame_id;
  pcl::toPCLPointCloud2(*pointcloud_chair, cloud_filtered);
  sensor_msgs::PointCloud2 chair;
  pcl_conversions::fromPCL(cloud_filtered, chair);

  // Publish the data
  pub.publish (chair);
  std::cout << "step6" << std::endl;


} 
  
  
int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "cluster_show_chair");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe ("/camera/depth/color/points", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
  pub = nh.advertise<sensor_msgs::PointCloud2> ("chair", 1);

  // Spin
  ros::spin ();
}
