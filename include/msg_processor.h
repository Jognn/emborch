//
// Created by jogn on 06.12.22.
//

#ifndef IOTPLATFORM_MSG_PROCESSOR_H
#define IOTPLATFORM_MSG_PROCESSOR_H

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

#endif //IOTPLATFORM_MSG_PROCESSOR_H
