//
// Created by jogn on 20.11.22.
//

#ifndef IOTPLATFORM_TESTSAMPLES_H
#define IOTPLATFORM_TESTSAMPLES_H

#include "stdint.h"

void benchmark_init(void);

void benchmark_setNextTimeSample(uint32_t value);

uint32_t benchmark_getTimeSample(unsigned index);

#endif //IOTPLATFORM_TESTSAMPLES_H
