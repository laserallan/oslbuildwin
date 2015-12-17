cmake_minimum_required(VERSION 2.8)
set (MY_INSTALL_PATH ${CMAKE_BINARY_DIR}/../../install)
set (CMAKE_INSTALL_PREFIX ${MY_INSTALL_PATH})

set(CMAKE_PREFIX_PATH ${MY_INSTALL_PATH};${MY_INSTALL_PATH}/install;../../boost_1_59_0)
set(BOOST_LIBRARYDIR D:/work/code/oslbuild/boost_1_59_0/lib64-msvc-12.0)
include_directories(${CMAKE_BINARY_DIR}/../../phase3/oiio/src/include)
add_subdirectory(oiio)