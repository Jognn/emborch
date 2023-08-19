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
#if DEBUG_MODE == 1
# define LUA_ENGINE_TASK_STACK_SIZE_B (LUA_BOARD_SPECIFIC_STACK_SIZE+THREAD_EXTRA_STACKSIZE_PRINTF)
#else
# define LUA_ENGINE_TASK_STACK_SIZE_B LUA_BOARD_SPECIFIC_STACK_SIZE
#endif

/* Interpreter stack size */
#if LUA_BOARD_SPECIFIC_INTERPRETER_SIZE == -1
# error "Invalid Lua interpter size"
#else
# define LUA_INTERPRETER_SIZE_B LUA_BOARD_SPECIFIC_INTERPRETER_SIZE
#endif

#endif //EMBORCH_DEFINITONS_H
