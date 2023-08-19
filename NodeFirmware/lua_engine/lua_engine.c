/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     module_lua_engine
 * @{
 *
 * @file
 * @brief       Lua Engine implementation
 *
 * @author      Jan Zobniow <jan.zobniow@gmail.com>
 *
 * @}
 */

/** Definitions */
#include "definitons.h"

#include "lua_engine.h"

/** System */
#include <errno.h>
#include <string.h>

/** Modules */
#include "lua_functions.h"
#include "msg_processor.h"
#include "lua_run.h"
#include "isrpipe.h"
#include "cond.h"


#define BUFFER_SIZE 512
extern cond_t luaScriptReady;
extern isrpipe_t luaPipe;
extern uint8_t luaPipeBuffer[BUFFER_SIZE];

static lua_State *runningLuaState = NULL;
static uint8_t currentLuaStatus = -1;
static uint8_t luaInterpreterMemory[LUA_INTERPRETER_SIZE_B] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

static struct callbackTable luaCallbacks[] = {
        {.functionCallback = l_initPin, .functionName="init_pin"},
        {.functionCallback = l_togglePin, .functionName = "toggle_pin"},
        {.functionCallback = l_sleep, .functionName = "sleep"},
        {.functionCallback = l_sleepMilli, .functionName = "sleep_ms"},
};

static void initCallbackTable(lua_State *L)
{
    for (unsigned i = 0; i < ARRAY_SIZE(luaCallbacks); ++i)
    {
        lua_pushcfunction(L, luaCallbacks[i].functionCallback);
        lua_setglobal(L, luaCallbacks[i].functionName);
    }
}

static int l_runScript(char const *const script, unsigned const scriptSize)
{
    runningLuaState = lua_riot_newstate(luaInterpreterMemory, sizeof(luaInterpreterMemory), NULL);
    if (runningLuaState == NULL)
    {
        LOG_DEBUG("[ERROR] Cannot create Lua state: not enough memory");
        return LUA_ERRMEM;
    }

    initCallbackTable(runningLuaState);

    int const loadBaseLibResult = lua_riot_openlibs(runningLuaState, LUAR_LOAD_BASE);
    if (loadBaseLibResult != LUAR_LOAD_O_ALL)
    {
        LOG_DEBUG("[ERROR] Trying to load library - %d\n", loadBaseLibResult);
        return LUA_ERRRUN;
    }

    luaL_loadbuffer(runningLuaState, script, scriptSize, "Main function");

    currentLuaStatus = LUA_OK;
    int const callResult = lua_pcall(runningLuaState, 0, 0, 0);

    // When we run into memory problems this condition won't pass and LUA_ERRMEM is returned
    if (callResult != LUA_OK)
    {
        LOG_DEBUG("[ERROR] Lua script running failed - %d\n", currentLuaStatus);
        runningLuaState = NULL;
        return callResult;
    }

    lua_close(runningLuaState);
    runningLuaState = NULL;
    return UINT8_MAX;
}

void luae_run(void)
{
    cond_wait(&luaScriptReady, &luaPipe.mutex);

    unsigned const size = tsrb_avail(&luaPipe.tsrb);
    LOG_DEBUG("Attempting to run the lua script");
    currentLuaStatus = UINT8_MAX;
    currentLuaStatus = l_runScript((const char *) luaPipeBuffer, size);
    LOG_DEBUG("Lua interpreter exited");

    char const *stack = thread_get_stackstart(thread_get_active());
    LOG_DEBUG("LUA_ENGINE STACK USAGE = %d\n", LUA_ENGINE_TASK_STACK_SIZE_B - thread_measure_stack_free(stack));
}

void luae_shutdown(void)
{
    if (runningLuaState != NULL)
    {
        LOG_DEBUG("Shutting down the lua engine!");
        lua_close(runningLuaState);
        memset(luaInterpreterMemory, 0, LUA_INTERPRETER_SIZE_B);
    }
}

uint8_t luae_getStatus(void)
{
    return currentLuaStatus;
}
