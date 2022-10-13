#include <stdio.h>
#include <errno.h>

/* Board stuff */
#include "include/board.h"
#include "include/thread.h"

/* Lua functions */
#include "include/lua_functions.h"

/* BLOB */
#include "bin/b-l072z-lrwan1/application_IoTPlatform/blobs/blob/main.lua.h"

/* Lua stack */
static char lua_stack[3000] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

/* CODE */
void *Lua_Task(void *arg)
{
    (void) arg;

    puts("Attempting to run main.lua");
    l_runScript(main_lua, main_lua_len);
    puts("Lua interpreter exited");

    return NULL;
}

int main(void)
{
    thread_create(
            lua_stack,
            sizeof(lua_stack),
            THREAD_PRIORITY_MAIN - 1,
            THREAD_CREATE_WOUT_YIELD | THREAD_CREATE_STACKTEST,
            Lua_Task,
            NULL,
            "LUA_TASK"
    );

    return 0;
}
