//
// Created by jogn on 20.11.22.
//

#include "include/benchmark_testSamples.h"

#ifdef IOTPLATFORM_TESTSAMPLES_H

#define SAMPLES_AMOUNT 10

static uint32_t measuredTimeSamples[SAMPLES_AMOUNT];
static uint32_t timeSamplesIndex = 0;

void benchmark_init(void)
{
    for(unsigned i = 0; i < SAMPLES_AMOUNT; ++i)
    {
        measuredTimeSamples[i] = 0;
    }
    timeSamplesIndex = 0;
}

void benchmark_setNextTimeSample(uint32_t value)
{
    if(timeSamplesIndex >= 10)
        return;

    measuredTimeSamples[timeSamplesIndex] = value;
    ++timeSamplesIndex;
}

uint32_t benchmark_getTimeSample(unsigned const index)
{
    if(index >= 10)
        return UINT32_MAX;

    return measuredTimeSamples[index];
}

#endif // IOTPLATFORM_TESTSAMPLES_H


