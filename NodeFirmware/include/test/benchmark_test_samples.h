/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#ifndef EMBORCH_TESTSAMPLES_H
#define EMBORCH_TESTSAMPLES_H


#include "stdint.h"


void benchmark_init(void);

void benchmark_setNextTimeSample(uint32_t value);

uint32_t benchmark_getTimeSample(unsigned index);

#endif // EMBORCH_TESTSAMPLES_H
