cmake_minimum_required(VERSION 2.8)
get_filename_component(ABS_INSTALL "${CMAKE_BINARY_DIR}/../../install" ABSOLUTE)
set (CMAKE_INSTALL_PREFIX ${ABS_INSTALL})
# Ignore warnings to increase signal to noise rate
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W0")
set(OSL_BUILD_PLUGINS 0)
add_subdirectory(llvm)