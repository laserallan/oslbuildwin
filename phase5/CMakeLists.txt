cmake_minimum_required(VERSION 2.8)
cmake_policy(SET CMP0004 NEW)
get_filename_component(ABS_INSTALL "${CMAKE_BINARY_DIR}/../../install" ABSOLUTE)
set (CMAKE_INSTALL_PREFIX ${ABS_INSTALL})
set(CMAKE_PREFIX_PATH ${ABS_INSTALL};${ABS_INSTALL}/install;../../boost_1_59_0)
#set(ABS_INSTALL D:/work/code/oslbuild/boost_1_59_0/lib64-msvc-12.0)
#include_directories(${CMAKE_BINARY_DIR}/../../phase3/oiio/src/include)
include_directories(${ABS_INSTALL}/include)
#set(BOOST_LIBRARYDIR ${ABS_INSTALL}/../downloads/boost/lib64-msvc-12.0)
set(BOOST_ROOT ${ABS_INSTALL}/../downloads/boost)
set(OSL_BUILD_CPP11 1)
set(USE_CPP11 1)
#set(LLVM_DIRECTORY ${ABS_INSTALL})
set(LLVM_FIND_QUIETLY 0)
set(LLVM_STATIC 1)
include_directories(${CMAKE_BINARY_DIR}/../../phase5/OpenShadingLanguage/src/include)
link_directories(${ABS_INSTALL}/lib)
set(FLEX_EXECUTABLE "${ABS_INSTALL}/bin/win_flex.exe")
set(BISON_EXECUTABLE "${ABS_INSTALL}/bin/win_bison.exe")
# Ignore warnings to increase signal to noise rate
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W0")
add_subdirectory(OpenShadingLanguage)
