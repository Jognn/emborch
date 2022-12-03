//
// Created by jogn on 13.10.22.
//
#ifndef IOTPLATFORM_LUA_FUNCTIONS_H
#define IOTPLATFORM_LUA_FUNCTIONS_H

#include "lauxlib.h"
#include "lualib.h"

struct callbackTable {
    lua_CFunction functionCallback;
    const char* functionName;
};

int l_runScript(char const * script, unsigned scriptSize);

int l_initPin(lua_State *L);

int l_togglePin(lua_State *L);

int l_sleep(lua_State *L);

int l_sleepMilli(lua_State *L);

#endif //IOTPLATFORM_LUA_FUNCTIONS_H
