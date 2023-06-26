/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */


/** Definitions */
#include "definitons.h"


#include "lua_functions.h"

/** Modules */
#include "periph/gpio.h"
#include "xtimer.h"


int l_initPin(lua_State *L)
{
    uint32_t const port = luaL_checkinteger(L, 1);
    uint32_t const pin = luaL_checkinteger(L, 2);
    bool const isInput = luaL_checkinteger(L, 3);

    int const result = gpio_init(GPIO_PIN(port, pin), isInput);
    lua_pushboolean(L, result == 0 ? true : false);

    return 1;
}

int l_togglePin(lua_State *L)
{
    uint32_t const port = luaL_checkinteger(L, 1);
    uint32_t const pin = luaL_checkinteger(L, 2);

    LOG_DEBUG("Toggling port: %lu pin: %lu\n", port, pin)
    gpio_toggle(GPIO_PIN(port, pin));

    return 0;
}

int l_sleep(lua_State *L)
{
    uint32_t const seconds = luaL_checkinteger(L, 1);
    LOG_DEBUG("Sleeping for %lu \n", seconds)
    xtimer_sleep(seconds);

    return 0;
}

int l_sleepMilli(lua_State *L)
{
    uint32_t const milliseconds = luaL_checkinteger(L, 1);
    LOG_DEBUG("Sleeping for %lu\n", milliseconds)
    xtimer_msleep(milliseconds);

    return 0;
}
