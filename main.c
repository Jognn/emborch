#include <stdio.h>
#include <errno.h>

/* Board stuff */
#include "include/board.h"
#include "include/gpio.h"
#include "include/xtimer.h"
#include "include/thread.h"

/* Lua headers */
#include "lauxlib.h"
#include "lualib.h"
#include "include/lua_run.h"

/* BLOB */
#include "bin/b-l072z-lrwan1/application_IoTPlatform/blobs/blob/main.lua.h"

#define LUA_MEM_SIZE (10*1024) // 11 kB

#define PH1_PIN GPIO_PIN(7, 0)

static char lua_mem[LUA_MEM_SIZE] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

static char lua_stack[3000] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

/* CODE */

static int hello(lua_State *L)
{
    (void) L;
    puts("hello function has been started");

    for(int i = 0; i < 10; ++i)
    {
        puts("TOGGLING THE PH1 PIN");
        gpio_toggle(PH1_PIN);
        xtimer_sleep(2);
    }
    return 0;
}

static int lua_run_script(uint8_t const * const script, size_t const scriptSize)
{
    lua_State *L = lua_riot_newstate(lua_mem, sizeof(lua_mem), NULL);

    if (L == NULL)
    {
        puts("Cannot create state: not enough memory");
        return ENOMEM;
    }

    lua_pushcfunction(L, hello);
    lua_setglobal(L, "hello");

    int const loadBaseLibResult = lua_riot_openlibs(L, LUAR_LOAD_BASE);
    if(loadBaseLibResult !=  LUAR_LOAD_O_ALL)
    {
        printf("An error has occurred when trying to load library - %d\n", loadBaseLibResult);
        return EINTR;
    }

    luaL_loadbuffer(L, (const char *)script, scriptSize, "Main function");

    int const pcallResult = lua_pcall(L, 0, 0, 0);
    if (pcallResult != LUA_OK)
    {
        puts("Lua script running failed");
        return EINTR;
    }

    lua_close(L);
    return 0;
}

void *Lua_Task(void *arg)
{
    (void) arg;
    gpio_init(PH1_PIN, GPIO_OUT);
    puts("Attempting to run main.lua");
    lua_run_script(main_lua, main_lua_len);
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
