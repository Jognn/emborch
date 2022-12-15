cmake_minimum_required(VERSION 3.23)
project(IoTPlatform C)

set(CMAKE_C_STANDARD 11)
set(BOARD nucleo-l476rg)

### RIOT INCLUDES BEGIN ###
include_directories($ENV{RIOT}/drivers/include/)
include_directories($ENV{RIOT}/core/include/)
include_directories($ENV{RIOT}/sys/include/)
include_directories($ENV{RIOT}/pkg/lua/include)
include_directories($ENV{RIOT}/boards/${BOARD}/include/)
include_directories(modules/lua_engine/include/)
### RIOT INCLUDES END ###

include_directories(include)

add_executable(IoTPlatform main.c lua_functions.c msg_processor.c lua_engine.c)
target_include_directories(IoTPlatform PUBLIC $ENV{RIOT})
add_subdirectory($ENV{RIOT} RIOT)

