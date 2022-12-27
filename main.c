//
// Created by jogn on 13.10.22
//

/* Definitions */
#include "definitons.h"

/* BLOB */
#include "bin/nucleo-l476rg/application_IoTPlatform/blobs/blob/main.lua.h"

/* Other */
#include "include/msg_processor.h"
#include "include/lua_engine.h"
#include "thread.h"
#include <errno.h>
#include <xtimer.h>

/* Lua engine stack */
static char luaEngineTaskStack[LUA_ENGINE_TASK_STACKSIZE] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

#if (NATIVE_TASK == 0)
/* CODE */
void* luaEngine(void *arg)
{
    (void) arg;

    while(true)
    {
        luae_run();
    }

    return NULL;
}
#endif

#if (NATIVE_TASK == 1)
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

void* msgProcessor(void *arg)
{
    (void) arg;

    while(true)
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
#if (NATIVE_TASK == 0)
    thread_create(
            luaEngineTaskStack,
            sizeof(luaEngineTaskStack),
            THREAD_PRIORITY_MAIN - 1,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            luaEngine,
            NULL,
            "LUA_TASK"
    );
    thread_create(
            stack,
            sizeof(stack),
            THREAD_PRIORITY_MAIN - 2,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            msgProcessor,
            NULL,
            "UART_CHECK"
    );
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
