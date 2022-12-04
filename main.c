#include <errno.h>

/* Board stuff */
#include "thread.h"

/* Lua functions */
#include "include/lua_functions.h"

/* BLOB */
#include "bin/nucleo-l476rg/application_IoTPlatform/blobs/blob/main.lua.h"

/* Other */
#include "definitons.h"
#include "string.h"

/* Lua stack */
static char luaEngineTaskStack[LUA_ENGINE_TASK_STACKSIZE] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

#if (NATIVE_TASK == 0)
/* CODE */
void* LuaEngine(void *arg)
{
    (void) arg;

    puts("Attempting to run main.lua");
    l_runScript((const char *)main_lua, main_lua_len);
    puts("Lua interpreter exited");
    const char* stack = thread_get_stackstart(thread_get_active());
    printf("LUA_ENGINE STACK USAGE = %d\n", LUA_ENGINE_TASK_STACKSIZE - thread_measure_stack_free(stack));

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

int main(void)
{
#if (NATIVE_TASK == 0)
    thread_create(
            luaEngineTaskStack,
            sizeof(luaEngineTaskStack),
            THREAD_PRIORITY_MAIN - 1,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            LuaEngine,
            NULL,
            "LUA_TASK"
    );
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
