//
// Created by jogn on 13.10.22.
//
#ifndef IOTPLATFORM_LUA_FUNCTIONS_H
#define IOTPLATFORM_LUA_FUNCTIONS_H

#include "lauxlib.h"
#include "lualib.h"

#define LUA_MEM_SIZE (10*1024) // 11 kB

struct callbackTable {
    lua_CFunction functionCallback;
    const char* functionName;
};

uint32_t l_getTimeSample(const uint32_t index);

int l_runScript(uint8_t const * script, size_t scriptSize);

int l_togglePin(lua_State *L);

int l_sleep(lua_State *L);

int l_sleepMili(lua_State *L);

#endif //IOTPLATFORM_LUA_FUNCTIONS_H
