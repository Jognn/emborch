/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */
#include "test/benchmark_test_samples.h"


#if (NATIVE_TEST_MODE == 1)

#define SAMPLES_AMOUNT 10

static uint32_t measuredTimeSamples[SAMPLES_AMOUNT];
static uint32_t timeSamplesIndex = 0;

void benchmark_init(void)
{
    for (unsigned i = 0; i < SAMPLES_AMOUNT; ++i)
    {
        measuredTimeSamples[i] = 0;
    }
    timeSamplesIndex = 0;
}

void benchmark_setNextTimeSample(uint32_t value)
{
    if (timeSamplesIndex >= 10)
        return;

    measuredTimeSamples[timeSamplesIndex] = value;
    ++timeSamplesIndex;
}

uint32_t benchmark_getTimeSample(unsigned const index)
{
    if (index >= 10)
        return UINT32_MAX;

    return measuredTimeSamples[index];
}

#endif // NATIVE_TEST_MODE == 1


