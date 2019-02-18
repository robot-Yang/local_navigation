#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/conversions.h>

#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/segmentation/extract_clusters.h>

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

  pcl::PointCloud<pcl::PointXYZ> point_cloud;
  pcl::PointCloud<pcl::PointXYZ>::Ptr point_cloudPtr(new pcl::PointCloud<pcl::PointXYZ>);
  pcl::fromPCLPointCloud2( cloud_filtered, point_cloud);
  pcl::copyPointCloud(point_cloud, *point_cloudPtr);

// Creating the KdTree object for the search method of the extraction
	pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>);
	tree->setInputCloud(point_cloudPtr);

	std::vector<pcl::PointIndices> cluster_indices;
	pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
	ec.setClusterTolerance(0.1); // 2cm
	ec.setMinClusterSize(100); //100
	ec.setMaxClusterSize(99000000);
	ec.setSearchMethod(tree);
	ec.setInputCloud(point_cloudPtr);
	ec.extract(cluster_indices);


  int i= 0;
  for (std::vector<pcl::PointIndices>::const_iterator it = clusters_indices.begin(); it != clusters_indices.end(); ++it)
  {
	  pcl::PointCloud<pcl::PointXYZ>::Ptr cluster(new pcl::PointCloud<pcl::PointXYZ>);

	  //创建新的点云数据集cloud_cluster，将所有当前聚类写入到点云数据集中 

	  for (std::vector<int>::const_iterator pit = it->indices.begin(); pit != it->indices.end(); ++pit)

	  cluster->points.push_back(cloud->points[*pit]);
	  cluster->width = cluster->points.size();
	  cluster->height = 1;
	  cluster->is_dense = true;

	  //保存聚类结果
	  if (cluster->points.size() <= 0)
		  break;

	  std::cout << "点云" << cluster->points.size() << "有这么多点" << std::endl;
	  std::stringstream ss;
	  ss << "索引" << j << ".pcd";
	  pcl::io::savePCDFile(ss.str(), *cluster);


	  i++;

  }
  
  
  
int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "cluster_write");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe ("/camera/depth_registered/points", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
  // pub = nh.advertise<sensor_msgs::PointCloud2> ("output", 1);

  // Spin
  ros::spin ();
}
