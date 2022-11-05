//
// Created by jogn on 31.10.22.
//

#ifndef IOTPLATFORM_NATIVE_TASK_H
#define IOTPLATFORM_NATIVE_TASK_H

#include "xtimer.h"

uint32_t native_getTimeSamples(uint32_t index);

void native_run(void);

int native_toggle(uint32_t port, uint32_t pin);

int native_sleepMili(int miliseconds);

int native_getTemperature(void);

#endif //IOTPLATFORM_NATIVE_TASK_H
