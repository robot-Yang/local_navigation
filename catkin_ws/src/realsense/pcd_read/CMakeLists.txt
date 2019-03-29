cmake_minimum_required(VERSION 2.8.3)
project(pcd_read)

set(PCL_DIR /usr/lib/x86_64-linux-gnu/cmake/pcl)

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

add_executable (pcd_read src/pcd_read.cpp)
target_link_libraries (pcd_read ${catkin_LIBRARIES} ${PCL_LIBRARIES})

# Install nodelet library
install(TARGETS ${PROJECT_NAME}
    ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    )

# Install header files
install(DIRECTORY include/
    DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
    )

# Install launch files
install(DIRECTORY launch/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
    )

# Install rviz files
install(DIRECTORY rviz/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/rviz
    )

# Install xml files
install(
    FILES nodelet_plugins.xml
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    )
