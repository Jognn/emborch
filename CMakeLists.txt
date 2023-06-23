cmake_minimum_required(VERSION 3.23)
project(emborch C)

set(CMAKE_C_STANDARD 11)
set(BOARD nucleo-l476rg)

add_compile_definitions(DEBUG_MODE=0 NATIVE_TEST_MODE=0)

include_directories(NodeFirmware/include)
include_directories(NodeFirmware/lua_engine)
include_directories(NodeFirmware/lua_engine/include)

### RIOT ###
include_directories($ENV{RIOT}/drivers/include/)
include_directories($ENV{RIOT}/core/include/)
include_directories($ENV{RIOT}/sys/include/)
include_directories($ENV{RIOT}/pkg/lua/include)
include_directories($ENV{RIOT}/boards/${BOARD}/include/)
add_subdirectory($ENV{RIOT} RIOT)
### RIOT END ###

add_subdirectory(NodeFirmware)

