//
// Created by jogn on 31.10.22.
//

#ifndef IOTPLATFORM_DEFINITONS_H
#define IOTPLATFORM_DEFINITONS_H

#include <stdio.h>

/* NATIVE TASK */
#define NATIVE_TASK 0

/* DEBUG_MODE */
#define DEBUG_MODE 0
#define LOG_DEBUG(...)  if(DEBUG_MODE == 1) { printf(__VA_ARGS__); }

/* LuaEngine task stack size */
#define LUA_ENGINE_TASK_STACKSIZE_DEFAULT 2000
#if DEBUG_MODE == 1
    #define LUA_ENGINE_TASK_STACKSIZE (LUA_ENGINE_TASK_STACKSIZE_DEFAULT+THREAD_EXTRA_STACKSIZE_PRINTF)
#else
    #define LUA_ENGINE_TASK_STACKSIZE LUA_ENGINE_TASK_STACKSIZE_DEFAULT
#endif

/* Interpreter stack size */
#define LUA_MEM_SIZE 14000 // 14 kB

#endif //IOTPLATFORM_DEFINITONS_H
