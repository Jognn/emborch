//
// Created by jogn on 13.10.22.
//
#include "definitons.h"

#if (NATIVE_TASK == 0)
#include "include/lua_functions.h"

#include "periph/gpio.h"
#include "xtimer.h"
#include "include/benchmark_testSamples.h"


int l_initPin(lua_State *L)
{
    uint32_t const port = luaL_checkinteger(L, 1);
    uint32_t const pin =  luaL_checkinteger(L, 2);
    bool const isInput = luaL_checkinteger(L, 3);

    int const result = gpio_init(GPIO_PIN(port, pin), isInput);
    lua_pushboolean(L, result == 0 ? true : false);

    return 1;
}

int l_togglePin(lua_State *L)
{
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

#endif // NATIVE_TASK == 0
