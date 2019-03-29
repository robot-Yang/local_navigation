cmake_minimum_required(VERSION 2.8.3)
project(train)

# we need FindFLANN.cmake
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR})

set(PCL_DIR /usr/lib/x86_64-linux-gnu/cmake/pcl)
set(HDF5_USE_STATIC_LIBRARIES ON)
set(HDF5_DIR /home/chen/Downloads/CMake-hdf5-1.10.4/build/HDF5-1.10.4-Linux/HDF_Group/HDF5/1.10.4/share/cmake/hdf5)
set(FLANN_DIR /home/chen/Software/flann-1.8.4-src/cmake)

#FIND_LIBRARY(HDF5_LIBRARY hdf5 /home/chen/Downloads/CMake-hdf5-1.10.4/build/HDF5-1.10.4-Linux/HDF_Group/HDF5/1.10.4/share/cmake)

#pkg_check_modules(flann REQUIRED flann hdf5)

find_package(catkin REQUIRED COMPONENTS
    message_generation
    roscpp
    sensor_msgs
    std_msgs
    nodelet
    cv_bridge
    image_transport
    tf
    dynamic_reconfigure
    diagnostic_updater
    pcl_conversions
    pcl_ros
    PCL REQUIRED
    HDF5 REQUIRED
    FLANN REQUIRED
    )

if(SET_USER_BREAK_AT_STARTUP)
	message("GOT FLAG IN CmakeLists.txt")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DBPDEBUG")
endif()

if (CMAKE_BUILD_TYPE EQUAL "RELEASE")
    message(STATUS "Create Release Build.")
    set(CMAKE_CXX_FLAGS "-O2 ${CMAKE_CXX_FLAGS}")
else()
    message(STATUS "Create Debug Build.")
endif()

set(CMAKE_CXX_FLAGS "-fPIE -fPIC -std=c++11 -D_FORTIFY_SOURCE=2 -fstack-protector -Wformat -Wformat-security -Wall ${CMAKE_CXX_FLAGS}")

#add_message_files(
#    FILES
#    IMUInfo.msg
#    Extrinsics.msg
#    )

generate_messages(
    DEPENDENCIES
    sensor_msgs
    std_msgs
    )

include_directories(
    include
    ${catkin_INCLUDE_DIRS}
    ${realsense_INCLUDE_DIR}
    ${PCL_INCLUDE_DIRS}
    )

include_directories(
    SYSTEM
    ${FLANN_INCLUDE_DIRS}
    ${HDF5_INCLUDE_DIR}
    )

# RealSense ROS Node
catkin_package(
    LIBRARIES ${PROJECT_NAME}
    CATKIN_DEPENDS message_runtime roscpp sensor_msgs std_msgs
    nodelet
    cv_bridge
    image_transport
    dynamic_reconfigure
    )


link_directories(${PCL_LIBRARY_DIRS})

add_definitions(${PCL_DEFINITIONS})

add_executable (train src/train.cpp)


target_link_libraries (train ${catkin_LIBRARIES}${PCL_LIBRARIES}${Boost_LIBRARIES}		    ${FLANN_LIBRARIES} ${HDF5_LIBRARY}${HDF5_hdf5_LIBRARY})


