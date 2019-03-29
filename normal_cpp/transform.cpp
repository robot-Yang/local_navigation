#include <pcl/common/impl/io.h>
#include <pcl/io/io.h>
#include <pcl/io/pcd_io.h>


int
main (int argc, char **argv)
{
    // load point cloud
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::io::loadPCDFile (argv[1], *cloud);
    pcl::PointCloud<pcl::PointNormal>::Ptr cloud_normal (new pcl::PointCloud<pcl::PointNormal>);
    pcl::copyPointCloud(*cloud, *cloud_normal);

    pcl::io::savePCDFileASCII (argv[2], *cloud_normal);
    
return (0);
}
