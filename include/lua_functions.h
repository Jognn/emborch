//
// Created by jogn on 13.10.22.
//
#ifndef IOTPLATFORM_LUA_FUNCTIONS_H

#include "lauxlib.h"
#include "lualib.h"

#define IOTPLATFORM_LUA_FUNCTIONS_H

int l_runScript(uint8_t const * script, size_t scriptSize);

int l_togglePin(lua_State *L);

int l_sleep(lua_State *L);




#endif //IOTPLATFORM_LUA_FUNCTIONS_H
