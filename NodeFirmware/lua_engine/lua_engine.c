/*
 * Copyright (C) 2022 Jognn
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

/** Modules */
#include "lua_functions.h"
#include "msg_processor.h"
#include "lua_run.h"
#include "isrpipe.h"
#include "cond.h"


extern cond_t luaScriptReady;
extern isrpipe_t luaPipe;
extern uint8_t luaPipeBuffer[BUFFER_SIZE];

static lua_State *runningLuaState = NULL;
static uint8_t luaInterpreterMemory[LUA_MEM_SIZE_BYTES] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

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
        puts("[ERROR] Cannot create Lua state: not enough memory");
        return ENOMEM;
    }

    initCallbackTable(runningLuaState);

    int const loadBaseLibResult = lua_riot_openlibs(runningLuaState, LUAR_LOAD_BASE);
    if (loadBaseLibResult != LUAR_LOAD_O_ALL)
    {
        printf("[ERROR] Trying to load library - %d\n", loadBaseLibResult);
        return EINTR;
    }

    luaL_loadbuffer(runningLuaState, script, scriptSize, "Main function");

    int const pcallResult = lua_pcall(runningLuaState, 0, 0, 0);

    // When we run into memory problems this condition won't pass and LUA_ERRMEM is returned
    if (pcallResult != LUA_OK)
    {
        printf("[ERROR] Lua script running failed - %d\n", pcallResult);
        return EINTR;
    }

    lua_close(runningLuaState);
    runningLuaState = NULL;
    return 0;
}

void luae_run(void)
{
    cond_wait(&luaScriptReady, &luaPipe.mutex);

    unsigned const size = tsrb_avail(&luaPipe.tsrb);
    printf("Script size - %d \n", size);

    puts("Attempting to run the lua script");
    l_runScript((const char *) luaPipeBuffer, size);
    puts("Lua interpreter exited");

    const char *stack = thread_get_stackstart(thread_get_active());
    printf("LUA_ENGINE STACK USAGE = %d\n", LUA_ENGINE_TASK_STACKSIZE_BYTES - thread_measure_stack_free(stack));
}

void luae_shutdown(void)
{
    if (runningLuaState != NULL)
    {
        puts("Shutting down the lua engine!");
        lua_close(runningLuaState);
    }
}
