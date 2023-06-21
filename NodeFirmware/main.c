/*
 * Copyright (C) 2022 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */


/** Definitions */
#include "definitons.h"

/** System */
#include <errno.h>
#include <xtimer.h>

/** Modules */
#include "lua_engine.h"
#include "thread.h"
#include "msg_processor.h"


/** Lua engine stack */
static char luaEngineTaskStack[LUA_ENGINE_TASK_STACKSIZE] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

#if (NATIVE_TEST_MODE == 0)

/** CODE */
void *luaEngine(void *arg)
{
    (void) arg;

    while (true)
    {
        luae_run();
    }

    return NULL;
}

#else
void* NativeTask(void *arg)
{
    (void) arg;
    benchmark_init();

    for(int i = 0; i < repetitions; ++i)
    {
        native_run();
    }

    for(int i = 0; i < repetitions; ++i)
    {
        printf("timeSamples[%d] = %lu us\n", i, benchmark_getTimeSample(i));
    }

    return NULL;
}
#endif

/* Message processor stack */
static char stack[1500] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

void *msgProcessor(void *arg)
{
    (void) arg;

    while (true)
    {
        msgp_checkUart();
    }

    return NULL;
}

void registerNode(void *arg)
{
    (void) arg;

    msgp_register();

}

int main(void)
{
    msgp_init();
#if (NATIVE_TEST_MODE == 0)
    thread_create(
            luaEngineTaskStack,
            sizeof(luaEngineTaskStack),
            THREAD_PRIORITY_MAIN - 1,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            luaEngine,
            NULL,
            "LUA_TASK");
    thread_create(
            stack,
            sizeof(stack),
            THREAD_PRIORITY_MAIN - 2,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            msgProcessor,
            NULL,
            "UART_CHECK");

    // Register 5 seconds after startup
    xtimer_sleep(5);
    msgp_register();

#else
    thread_create(
            luaEngineTaskStack,
            sizeof(luaEngineTaskStack),
            THREAD_PRIORITY_MAIN - 1,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            NativeTask,
            NULL,
            "NATIVE_TASK"
    );
#endif
    return 0;
}
