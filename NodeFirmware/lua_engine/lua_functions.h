/*
 * Copyright (C) 2022 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#ifndef EMBORCH_LUA_FUNCTIONS_H
#define EMBORCH_LUA_FUNCTIONS_H


#include "lauxlib.h"
#include "lualib.h"


struct callbackTable
{
    lua_CFunction functionCallback;
    const char *functionName;
};

int l_initPin(lua_State *L);

int l_togglePin(lua_State *L);

int l_sleep(lua_State *L);

int l_sleepMilli(lua_State *L);

#endif // EMBORCH_LUA_FUNCTIONS_H
