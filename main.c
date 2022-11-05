#include <stdio.h>
#include <errno.h>

/* Board stuff */
#include "include/board.h"
#include "include/thread.h"

/* Lua functions */
#include "include/lua_functions.h"

/* BLOB */
#include "bin/b-l072z-lrwan1/application_IoTPlatform/blobs/blob/main.lua.h"

#include "native_task.h"
#include "debug.h"

/* Lua stack */
#define STACK_SIZE 2000
static char luaEngineTaskStack[STACK_SIZE] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

/* CODE */
void* LuaEngine(void *arg)
{
    (void) arg;

    int const repetitions = 5;

    for(int i = 0; i < repetitions; ++i)
    {
        puts("Attempting to run main.lua");
        l_runScript(main_lua, main_lua_len);
        puts("Lua interpreter exited");
        const char* stack = thread_get_stackstart(thread_get_active());
        printf("STACK USAGE %d, = %d\n", i, STACK_SIZE - thread_measure_stack_free(stack));
    }


    for(int i = 0; i < repetitions; ++i)
    {
        printf("timeSamples[%d] = %lu us\n", i, l_getTimeSample(i));
    }

    return NULL;
}

void* NativeTask(void *arg)
{
    (void) arg;

    for(int i = 0; i < 5; ++i)
    {
        native_run();
    }

    for(int i = 0; i < 5; ++i)
    {
        printf("timeSamples[%d] = %lu us\n", i, native_getTimeSamples(i));
    }

    return NULL;
}

int main(void)
{
    thread_create(
            luaEngineTaskStack,
            sizeof(luaEngineTaskStack),
            THREAD_PRIORITY_MAIN - 1,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            LuaEngine,
            NULL,
            "LUA_TASK"
    );

//    thread_create(
//            luaEngineTaskStack,
//            sizeof(luaEngineTaskStack),
//            THREAD_PRIORITY_MAIN - 1,
//            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
//            NativeTask,
//            NULL,
//            "NATIVE_TASK"
//    );
    return 0;
}
