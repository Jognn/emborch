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
#define INITIAL_ID 0


typedef enum
{
    eMessageTypeRegister = 0,
    eMessageTypeSendScript = 1,
    eMessageTypeMonitor = 2,
    eMessageTypeNotSet
} MessageType;

typedef struct __attribute__((packed))
{
    uint8_t messageType: 4;
    uint8_t senderId: 4;
} MessageHeader;


/** Register messages */
typedef struct __attribute__((packed))
{
    MessageHeader messageHeader;
    uint8_t assignedId;
} MessageRegister_Orchestrator;

typedef union __attribute__((packed))
{
    struct
    {
        MessageHeader messageHeader;
        uint8_t availableMemory_kB;
        uint16_t supportedFeatures;
    };
    uint8_t bytes[4];
} MessageRegister_Node;


/** Send script messages */

/*
 * MessageSendScript_Orchestrator - skipped for now
 */


void msgp_init(void);

void msgp_pollMessages(void);

void msgp_register(void);

#endif // EMBORCH_MSG_PROCESSOR_H
