cmake_minimum_required(VERSION 3.23)
project(IoTPlatform C)

set(CMAKE_C_STANDARD 11)

include_directories(../RIOT/)

add_executable(IoTPlatform main.c include/board.h)
