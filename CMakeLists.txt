cmake_minimum_required(VERSION 3.23)
project(emborch C)

set(CMAKE_C_STANDARD 11)
set(BOARD nucleo-l476rg)

add_compile_definitions(DEBUG_MODE=0 NATIVE_TEST_MODE=0)

if (BOARD STREQUAL "nucleo-l476rg")
    message("BOARD: nucleo-l476rg")
    set(
            LUA_INTERPRETER_SIZE_B=14000
            LUA_ENGINE_TASK_SIZE_B=2000
            FEATURES=1
    )
elseif (BOARD STREQUAL "nucleo-f722ze")
    message("BOARD: nucleo-f722ze")
    set(
            LUA_INTERPRETER_SIZE_B=20000
            LUA_ENGINE_TASK_SIZE_B=2000
            FEATURES=1
    )
else ()
    message("BOARD: UNKNOWN")
    set(
            LUA_INTERPRETER_SIZE_B=-1
            LUA_ENGINE_TASK_SIZE_B=-1
            FEATURES=-1
    )
endif ()
add_compile_definitions(
        LUA_BOARD_SPECIFIC_INTERPRETER_SIZE=LUA_INTERPRETER_SIZE_B
        LUA_BOARD_SPECIFIC_STACK_SIZE=LUA_ENGINE_TASK_SIZE_B
        FEATURE_BITSET=FEATURES)

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

