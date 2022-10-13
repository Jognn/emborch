//
// Created by jogn on 13.10.22.
//
#include <stdio.h>
#include <errno.h>

#include "include/xtimer.h"
#include "include/gpio.h"
#include "include/lua_functions.h"
#include "include/lua_run.h"

#define LUA_MEM_SIZE (10*1024) // 11 kB
static char lua_mem[LUA_MEM_SIZE] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));


int l_runScript(uint8_t const * const script, size_t const scriptSize)
{
    lua_State *L = lua_riot_newstate(lua_mem, sizeof(lua_mem), NULL);
    if (L == NULL)
    {
        puts("Cannot create state: not enough memory");
        return ENOMEM;
    }

    lua_pushcfunction(L, l_togglePin);
    lua_setglobal(L, "toggle_pin");

    lua_pushcfunction(L, l_sleep);
    lua_setglobal(L, "sleep");

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

int l_togglePin(lua_State *L)
{
    (void) L;

    uint32_t const port = luaL_checkinteger(L, 1);
    uint32_t const pin =  luaL_checkinteger(L, 2);

    gpio_init(GPIO_PIN(port, pin), GPIO_OUT);
    printf("Toggle port - %lu pin - %lu\n", port, pin);
    gpio_toggle(GPIO_PIN(port, pin));

    return 0;
}

int l_sleep(lua_State *L)
{
    uint32_t const seconds = luaL_checkinteger(L, 1);
    printf("Sleeping for %lu seconds\n", seconds);
    xtimer_sleep(seconds);

    return 0;
}
