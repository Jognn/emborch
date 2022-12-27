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

typedef struct
{
    MessageType messageType;
    uint8_t message_sender : 4;
    uint8_t available_memory;
    uint8_t end;
} RegisterMessage;

void msgp_init(void);

void msgp_checkUart(void);

void msgp_register(void);

#endif //IOTPLATFORM_MSG_PROCESSOR_H
