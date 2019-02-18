     #include <pcl/io/io.h>
     #include <pcl/io/pcd_io.h>
     #include <pcl/features/integral_image_normal.h>
     #include <pcl/visualization/cloud_viewer.h>

     int
     main (int argc, char **argv)
     {
             // load point cloud
             pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
             pcl::io::loadPCDFile (argv[1], *cloud);

             // estimate normals
             pcl::PointCloud<pcl::Normal>::Ptr normals (new pcl::PointCloud<pcl::Normal>);

             pcl::IntegralImageNormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
             ne.setNormalEstimationMethod (ne.AVERAGE_3D_GRADIENT);
             ne.setMaxDepthChangeFactor(0.02f);
             ne.setNormalSmoothingSize(10.0f);
             ne.setInputCloud(cloud);
             ne.compute(*normals);

             // visualize normals
             pcl::visualization::PCLVisualizer viewer("PCL Viewer");
             viewer.setBackgroundColor (0.0, 0.0, 0.5);
             viewer.addPointCloudNormals<pcl::PointXYZ,pcl::Normal>(cloud, normals);

             while (!viewer.wasStopped ())
             {
               viewer.spinOnce ();
             }
             return 0;
     }
