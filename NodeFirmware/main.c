/*
 * Copyright (C) 2023 Jognn
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
static char luaEngineTaskStack[LUA_ENGINE_TASK_STACK_SIZE_B] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

#if (NATIVE_TEST_MODE == 0)

/** CODE */
void *task_luaEngine(void *arg)
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

void *task_msgProcessor(void *arg)
{
    (void) arg;

    msgp_init();
    // Wait 5 seconds before sending the register message
    xtimer_sleep(5);
    puts("SENDING REGISTER MESSAGE");
    msgp_register();

    while (true)
    {
        msgp_pollMessages();
    }

    return NULL;
}

int main(void)
{
#if (NATIVE_TEST_MODE == 0)
    thread_create(
            stack,
            sizeof(stack),
            THREAD_PRIORITY_MAIN - 2,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            task_msgProcessor,
            NULL,
            "MSG_PROCESSOR");
    thread_create(
            luaEngineTaskStack,
            sizeof(luaEngineTaskStack),
            THREAD_PRIORITY_MAIN - 1,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            task_luaEngine,
            NULL,
            "LUA_TASK");

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
