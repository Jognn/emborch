//
// Created by jogn on 13.10.22.
//
#include "include/lua_functions.h"

#include "include/gpio.h"
#include "include/xtimer.h"
#include "include/lua_run.h"

#include <errno.h>
#include <stdlib.h>
#include "include/debug.h"

static char luaMem[LUA_MEM_SIZE] __attribute__ ((aligned(__BIGGEST_ALIGNMENT__)));

static uint32_t measuredTimeSamples[10];
static uint32_t timeSamplesIndex = 0;

uint32_t l_getTimeSample(uint32_t const index)
{
    if(index >= 10)
        return UINT32_MAX;

    return measuredTimeSamples[index];
}

static struct callbackTable luaCallbacks[] = {
        { .functionCallback = l_togglePin, .functionName = "toggle_pin" },
        { .functionCallback = l_sleep, .functionName = "sleep" },
        { .functionCallback = l_sleepMilli, .functionName = "sleep_ms" },
        { .functionCallback = l_getTemperatureMock, .functionName = "get_temperature"},
};

static void initCallbackTable(lua_State *L)
{
    for (unsigned i = 0; i < ARRAY_SIZE(luaCallbacks); ++i)
    {
        lua_pushcfunction(L, luaCallbacks[i].functionCallback);
        lua_setglobal(L, luaCallbacks[i].functionName);
    }
}

static int number = 0;

int l_runScript(uint8_t const * const script, size_t const scriptSize)
{
    lua_State *L = lua_riot_newstate(luaMem, sizeof(luaMem), NULL);
    if (L == NULL)
    {
        puts("Cannot create Lua state: not enough memory");
        return ENOMEM;
    }

    initCallbackTable(L);

    gpio_init(GPIO_PIN(7, 0), GPIO_OUT);
    number = 0;

    int const loadBaseLibResult = lua_riot_openlibs(L, LUAR_LOAD_BASE);
    if(loadBaseLibResult !=  LUAR_LOAD_O_ALL)
    {
        printf("An error has occurred when trying to load library - %d\n", loadBaseLibResult);
        return EINTR;
    }

    luaL_loadbuffer(L, (const char *)script, scriptSize, "Main function");

    uint32_t const start = xtimer_now_usec();
    int const pcallResult = lua_pcall(L, 0, 0, 0);
    uint32_t const stop = xtimer_now_usec();

    measuredTimeSamples[timeSamplesIndex] = stop - start;
    ++timeSamplesIndex;

    if (pcallResult != LUA_OK)
    {
        puts("Lua script running failed");
        return EINTR;
    }

    lua_close(L);
    return 0;
}

int l_getTemperatureMock(lua_State *L)
{
    lua_pushnumber(L, rand());
    return 1;
}

int l_togglePin(lua_State *L)
{
    (void) L;

    uint32_t const port = luaL_checkinteger(L, 1);
    uint32_t const pin =  luaL_checkinteger(L, 2);

    LOG_DEBUG("Toggling port: %lu pin: %lu\n", port, pin)
    gpio_toggle(GPIO_PIN(port, pin));

    return 0;
}

int l_sleep(lua_State *L)
{
    uint32_t const seconds = luaL_checkinteger(L, 1);
    LOG_DEBUG("Sleeping for %lus \n", seconds)
    xtimer_sleep(seconds);

    return 0;
}

int l_sleepMilli(lua_State *L)
{
    uint32_t const milliseconds = luaL_checkinteger(L, 1);
    LOG_DEBUG("Sleeping for %lums\n", milliseconds)
    xtimer_msleep(milliseconds);

    return 0;
}
