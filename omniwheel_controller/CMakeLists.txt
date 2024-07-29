cmake_minimum_required(VERSION 3.0.2)
project(omniwheel_controller)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

catkin_package()

include_directories(include ${catkin_INCLUDE_DIRS})

SET(
  SRC_FILES
  src/LowLevelController.cpp
)

add_library(${PROJECT_NAME} ${SRC_FILES})
add_executable(test_algo src/main.cpp)
target_link_libraries(test_algo ${catkin_LIBRARIES} ${PROJECT_NAME})

