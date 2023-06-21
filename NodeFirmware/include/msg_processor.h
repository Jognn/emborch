/*
 * Copyright (C) 2022 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#ifndef EMBORCH_MSG_PROCESSOR_H
#define EMBORCH_MSG_PROCESSOR_H


#include <stdint.h>


#define BUFFER_SIZE 512

typedef enum
{
    eMessageTypeRegister,
    eMessageTypeSendScript,
    eMessageTypeAliveCheck,
    eMessageTypeReport,
    eMessageTypeNotSet
} MessageType;


void msgp_init(void);

void msgp_checkUart(void);

void msgp_register(void);

#endif // EMBORCH_MSG_PROCESSOR_H
