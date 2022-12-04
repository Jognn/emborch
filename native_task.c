//
// Created by jogn on 31.10.22.
//

#include "definitons.h"

#if (NATIVE_TASK == 1)

#include "include/native_task.h"

#include "include/xtimer.h"
#include "include/gpio.h"
#include "include/benchmark_testSamples.h"
#include "stdlib.h"

#define RAND_ARRAY \
{ \
{rand()%6,rand()%6,rand()%6,rand()%6,rand()%6,rand()%6}, \
{rand()%6,rand()%6,rand()%6,rand()%6,rand()%6,rand()%6}, \
{rand()%6,rand()%6,rand()%6,rand()%6,rand()%6,rand()%6}, \
{rand()%6,rand()%6,rand()%6,rand()%6,rand()%6,rand()%6}, \
{rand()%6,rand()%6,rand()%6,rand()%6,rand()%6,rand()%6}, \
{rand()%6,rand()%6,rand()%6,rand()%6,rand()%6,rand()%6} \
}


static void led_blinking(void)
{
    for (int j = 1; j <= 4; ++j)
    {
        native_toggle(7, 0);
        native_sleepMilli(500);
    }
}

static void matrix_multiplication(void)
{
#define M 6
    long a[M][M] = RAND_ARRAY;
    long b[M][M] = RAND_ARRAY;
    long c[M][M] = RAND_ARRAY;

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
    int const AMOUNT_OF_SAMPLES = 5;

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
    srand(xtimer_now_usec());
    uint32_t const start = xtimer_now_usec();
    integerAvgTemperature();
    uint32_t const stop = xtimer_now_usec();

    // Benchmark tests - time execution
    benchmark_setNextTimeSample(stop - start);
}

int native_toggle(uint32_t const port, uint32_t const pin)
{
    LOG_DEBUG("Toggling port: %lu pin: %lu\n", port, pin)
    gpio_toggle(GPIO_PIN(port, pin));
    return 0;
}

int native_sleepMilli(int const milliseconds)
{
    xtimer_msleep(milliseconds);
    return 0;
}

int native_getTemperature()
{
    return rand()%10;
}

#endif // NATIVE_TASK == 0


