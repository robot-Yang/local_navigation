#include <Eigen/Core>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/common/time.h>
#include <pcl/console/print.h>
#include <pcl/features/normal_3d_omp.h>
#include <pcl/features/fpfh_omp.h>
#include <pcl/filters/filter.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/io/pcd_io.h>
#include <pcl/registration/icp.h>
#include <pcl/registration/sample_consensus_prerejective.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
// Types
typedef pcl::PointNormal PointNT;
typedef pcl::PointCloud<PointNT> PointCloudT;
typedef pcl::FPFHSignature33 FeatureT;
typedef pcl::FPFHEstimationOMP<PointNT, PointNT, FeatureT> FeatureEstimationT;
typedef pcl::PointCloud<FeatureT> FeatureCloudT;
typedef pcl::visualization::PointCloudColorHandlerCustom<PointNT> ColorHandlerT;
 
//handle the param of the align in the txt to save the fucking time of complie
int parseConfigFile(
    const std::string &filepath,
    char *objFile,
    char *sceFile,
    float *downLeaf
);
 
 
// Align a rigid object to a scene with clutter and occlusions
int main(int argc, char **argv)
{
    // Point clouds
    PointCloudT::Ptr object(new PointCloudT);
    PointCloudT::Ptr object_aligned(new PointCloudT);
    PointCloudT::Ptr scene(new PointCloudT);
    FeatureCloudT::Ptr object_features(new FeatureCloudT);
    FeatureCloudT::Ptr scene_features(new FeatureCloudT);
 
    // Get input object and scene
    /*if (argc != 3)
    {
    pcl::console::print_error("Syntax is: %s object.pcd scene.pcd\n", argv[0]);
    return (1);
    }*/
    /*std::string paramFilePath = "data/param.txt";
    char *obj_filepath = { '\0' };
    char *sce_filepath = { '\0' };
    float *downsample_leaf = nullptr;
    parseConfigFile(
    paramFilePath,
    obj_filepath,
    sce_filepath,
    downsample_leaf
    );*/
 
 
    // Load object and scene
    pcl::console::print_highlight("Loading point clouds...\n");
    if (pcl::io::loadPCDFile<PointNT>("data/obj_seg.pcd", *object) < 0 ||//"data/obj_seg.pcd"
        pcl::io::loadPCDFile<PointNT>("data/sce_seg.pcd", *scene) < 0)   //"data/sce_seg.pcd"
    {
        pcl::console::print_error("Error loading object/scene file!\n");
        return (1);
    }
 
    // Downsample
    pcl::console::print_highlight("Downsampling...\n");
    pcl::VoxelGrid<PointNT> grid;
    const float leaf = 0.08f;//0.005f == resolution of 5mm
    grid.setLeafSize(leaf, leaf, leaf);
    grid.setInputCloud(object);
    grid.filter(*object);
    grid.setInputCloud(scene);
    grid.filter(*scene);
 
    // Estimate normals for scene
    pcl::console::print_highlight("Estimating scene normals...\n");
    pcl::NormalEstimationOMP<PointNT, PointNT> nest;
    nest.setRadiusSearch(0.01);
    nest.setInputCloud(scene);
    nest.compute(*scene);
 
    // Estimate features
    pcl::console::print_highlight("Estimating features...\n");
    FeatureEstimationT fest;
    fest.setRadiusSearch(0.025);
    fest.setInputCloud(object);
    fest.setInputNormals(object);
    fest.compute(*object_features);
    fest.setInputCloud(scene);
    fest.setInputNormals(scene);
    fest.compute(*scene_features);
 
    // Perform alignment
    pcl::console::print_highlight("Starting alignment...\n");
    pcl::SampleConsensusPrerejective<PointNT, PointNT, FeatureT> align;
    align.setInputSource(object);
    align.setSourceFeatures(object_features);
    align.setInputTarget(scene);
    align.setTargetFeatures(scene_features);
    align.setMaximumIterations(100000); // Number of RANSAC iterations 50000
    align.setNumberOfSamples(3); // Number of points to sample for generating/prerejecting a pose
    align.setCorrespondenceRandomness(5); // Number of nearest features to use
    align.setSimilarityThreshold(0.9f); // Polygonal edge length similarity threshold
    align.setMaxCorrespondenceDistance(2.5f * leaf); // Inlier threshold
    align.setInlierFraction(0.25f); // Required inlier fraction for accepting a pose hypothesis
    {
        pcl::ScopeTime t("Alignment");
        align.align(*object_aligned);
    }
 
    if (align.hasConverged())
    {
        // Print results
        printf("\n");
        Eigen::Matrix4f transformation = align.getFinalTransformation();
        pcl::console::print_info("    | %6.3f %6.3f %6.3f | \n", transformation(0, 0), transformation(0, 1), transformation(0, 2));
        pcl::console::print_info("R = | %6.3f %6.3f %6.3f | \n", transformation(1, 0), transformation(1, 1), transformation(1, 2));
        pcl::console::print_info("    | %6.3f %6.3f %6.3f | \n", transformation(2, 0), transformation(2, 1), transformation(2, 2));
        pcl::console::print_info("\n");
        pcl::console::print_info("t = < %0.3f, %0.3f, %0.3f >\n", transformation(0, 3), transformation(1, 3), transformation(2, 3));
        pcl::console::print_info("\n");
        pcl::console::print_info("Inliers: %i/%i\n", align.getInliers().size(), object->size());
 
        // Show alignment
        pcl::visualization::PCLVisualizer visu("Alignment");
        visu.addPointCloud(scene, ColorHandlerT(scene, 0.0, 255.0, 0.0), "scene");
        visu.addPointCloud(object_aligned, ColorHandlerT(object_aligned, 0.0, 0.0, 255.0), "object_aligned");
        visu.spin();
        system("PAUSE");
    }
    else
    {
        pcl::console::print_error("Alignment failed!\n");
        system("PAUSE");
        return (1);
    }
 
    return (0);
}
 
int parseConfigFile(
    const std::string &filepath,
    char *objFile,
    char *sceFile,
    float *downLeaf
)
{
    // open the configuration file
    FILE *file = fopen(filepath.c_str(), "r");
    //FILE *stream;//test
    if (!file)
    {
        fprintf(stderr, "Cannot parse configuration file \"%s\".\n",
            filepath.c_str());
        exit(1);
    }
    //read parameters
    char buf[256];
    while (fscanf(file, "%s", buf) != EOF) {
        switch (buf[0]) {
        case '#':
            fgets(buf, sizeof(buf), file);
            break;
        case'o':
            fgets(buf, sizeof(buf), file);
            memcpy(objFile, buf + 1, strlen(buf) - 2);
            //printf("%s", objFile);
            break;
        case's':
            fgets(buf, sizeof(buf), file);
            memcpy(sceFile, buf + 1, strlen(buf) - 2);
            break;
        case'l':
            fscanf(file, "%f", downLeaf);
        }
    }
    return 0;
 
}　
