/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */


/** Modules */
#include "lua_engine.h"
#include "thread.h"
#include "msg_processor.h"


#if (NATIVE_TEST_MODE == 1)
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

int main(void)
{
#if !NATIVE_TEST_MODE
    msgp_init();
    luae_init();
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
