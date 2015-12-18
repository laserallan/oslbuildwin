cmake_minimum_required(VERSION 2.8)
get_filename_component(ABS_INSTALL "${CMAKE_BINARY_DIR}/../../install" ABSOLUTE)
set (CMAKE_INSTALL_PREFIX ${ABS_INSTALL})

set(CMAKE_PREFIX_PATH ${ABS_INSTALL};${ABS_INSTALL}/install;../../boost_1_59_0)
set(BOOST_LIBRARYDIR  ${ABS_INSTALL}/../downloads/boost/lib64-msvc-12.0)
set(BOOST_ROOT  ${ABS_INSTALL}/../downloads/boost)
include_directories(${CMAKE_BINARY_DIR}/../../phase3/oiio/src/include)
add_subdirectory(oiio)