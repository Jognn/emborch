//
// Created by jogn on 31.10.22.
//

#ifndef IOTPLATFORM_NATIVE_TASK_H
#define IOTPLATFORM_NATIVE_TASK_H

#include "xtimer.h"

void native_run(void);

int native_toggle(uint32_t port, uint32_t pin);

int native_sleepMilli(int milliseconds);

int native_getTemperature(void);

#endif //IOTPLATFORM_NATIVE_TASK_H
