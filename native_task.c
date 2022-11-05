//
// Created by jogn on 31.10.22.
//

#include "include/native_task.h"

#include "include/debug.h"

#include "include/xtimer.h"
#include "include/gpio.h"

uint32_t measuredTimeSamples[10];
uint32_t timeSamplesIndex = 0;
static int number = 0;

uint32_t native_getTimeSamples(uint32_t const index)
{
    if (index >= 10)
        return UINT32_MAX;

    return measuredTimeSamples[index];
}

static void led_blinking(void)
{
    for (int j = 1; j <= 4; ++j)
    {
        native_toggle(7, 0);
        native_sleepMili(500);
    }
}

static void matrix_multiplication(void)
{
#define M 6

    long a[M][M] =
    {{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6}};
    long b[M][M] = {{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6},{1,2,3,4,5,6}};
    long c[M][M] = {{0,0,0,0,0,0}, {0,0,0,0,0,0}, {0,0,0,0,0,0}, {0,0,0,0,0,0}, {0,0,0,0,0,0}, {0,0,0,0,0,0}};

    for (int i = 0; i < M; ++i)
    {
        for (int j = 0; j < M; ++j)
        {
            long temp = 0;
            for (int k = 0; k < M; ++k)
            {
                temp += a[i][k] * b[k][j];
            }
            c[i][j] = temp;
        }
    }
}

static double integerAvgTemperature(void)
{
    int const AMOUNT_OF_SAMPLES = 75;

    int temperatureSamples[AMOUNT_OF_SAMPLES];
    double sum = 0;

    for (int i = 0; i < AMOUNT_OF_SAMPLES; ++i)
    {
        int const temperature = native_getTemperature();
        temperatureSamples[i] = temperature;
        sum += temperature;
    }

    return sum/AMOUNT_OF_SAMPLES;
}

void native_run(void)
{
    uint32_t const start = xtimer_now_usec();
    integerAvgTemperature();
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

int native_getTemperature()
{
    return ++number;;
}


