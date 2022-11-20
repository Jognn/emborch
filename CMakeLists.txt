cmake_minimum_required(VERSION 3.23)
project(IoTPlatform C)

set(CMAKE_C_STANDARD 11)

include_directories(../RIOT/)

include_directories(include)

add_executable(IoTPlatform main.c lua_functions.c native_task.c benchmark_testSamples.c)

target_include_directories(IoTPlatform PUBLIC ../RIOT)
add_subdirectory(../RIOT RIOT)
