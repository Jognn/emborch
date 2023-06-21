/*
 * Copyright (C) 2022 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#ifndef IOTPLATFORM_NATIVE_TASK_H
#define IOTPLATFORM_NATIVE_TASK_H

#include "xtimer.h"

void native_run(void);

int native_toggle(uint32_t port, uint32_t pin);

int native_sleepMilli(int milliseconds);

int native_getTemperature(void);

#endif //IOTPLATFORM_NATIVE_TASK_H
