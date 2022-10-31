//
// Created by jogn on 31.10.22.
//

#include "include/native_task.h"

#include "include/debug.h"

#include "include/xtimer.h"
#include "include/gpio.h"

uint32_t measuredTimeSamples[10];
uint32_t timeSamplesIndex = 0;

uint32_t native_getTimeSamples(uint32_t const index)
{
    if (index >= 10)
        return UINT32_MAX;

    return measuredTimeSamples[index];
}

static void native_code(void)
{
    for (int j = 1; j <= 4; ++j)
    {
        native_toggle(7, 0);
        native_sleepMili(500);
    }
}

void native_run(void)
{
    uint32_t const start = xtimer_now_usec();
    native_code();
    uint32_t const stop = xtimer_now_usec();

    measuredTimeSamples[timeSamplesIndex] = stop - start;
    ++timeSamplesIndex;
}

int native_toggle(uint32_t const port, uint32_t const pin)
{
    LOG_DEBUG("Toggling port: %lu pin: %lu\n", port, pin)
    gpio_toggle(GPIO_PIN(port, pin));
    return 0;
}

int native_sleepMili(int const miliseconds)
{
    xtimer_msleep(miliseconds);
    return 0;
}


