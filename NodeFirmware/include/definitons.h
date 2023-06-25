/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#ifndef EMBORCH_DEFINITONS_H
#define EMBORCH_DEFINITONS_H


#include <stdio.h>

/* DEBUG_MODE */
#define LOG_DEBUG(...)  if(DEBUG_MODE == 1) { printf(__VA_ARGS__); }

/* LuaEngine task stack size */
#define LUA_ENGINE_TASK_STACKSIZE_DEFAULT_BYTES 2000
#if DEBUG_MODE == 1
#define LUA_ENGINE_TASK_STACKSIZE (LUA_ENGINE_TASK_STACKSIZE_DEFAULT+THREAD_EXTRA_STACKSIZE_PRINTF)
#else
#define LUA_ENGINE_TASK_STACKSIZE_BYTES LUA_ENGINE_TASK_STACKSIZE_DEFAULT_BYTES
#endif

/* Interpreter stack size */
#define LUA_MEM_SIZE_BYTES 14000

#endif //EMBORCH_DEFINITONS_H
