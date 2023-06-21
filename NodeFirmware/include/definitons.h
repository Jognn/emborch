/*
 * Copyright (C) 2022 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#ifndef IOTPLATFORM_DEFINITONS_H
#define IOTPLATFORM_DEFINITONS_H


#include <stdio.h>

/* NATIVE TASK */
//#define NATIVE_TEST_MODE 0

/* DEBUG_MODE */
//#define DEBUG_MODE 0
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
