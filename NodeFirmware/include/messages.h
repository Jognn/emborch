/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#ifndef EMBORCH_MESSAGES_H
#define EMBORCH_MESSAGES_H


#include <stdint.h>


#define BUFFER_SIZE 512

/** Message header */
#define MESSAGE_TYPE_MASK 0xF0
typedef uint8_t MessageHeader;

typedef enum
{
    eMessageTypeRegister = 0,
    eMessageTypeSendScript = 1,
    eMessageTypeMonitor = 2,
    eMessageTypeNotSet
} MessageType;

#define INITIAL_ID 0
#define MESSAGE_SENDER_MASK 0x0F

/** Register messages */
typedef struct __attribute__((packed))
{
    uint8_t assignedId;
} MessageRegister_Orchestrator;

typedef union __attribute__((packed))
{
    struct
    {
        uint8_t availableMemory_kB;
        uint16_t supportedFeatures;
    };
    uint8_t bytes[3];
} MessageRegister_Node;


/** Send script messages */
/*
 * MessageSendScript_Orchestrator - skipped for now
 */


/** Monitor messages */
typedef union __attribute__((packed))
{
    struct
    {
        uint8_t currentLuaStatus;
    };
    uint8_t bytes[1];
} MessageMonitor_Node;

#endif //EMBORCH_MESSAGES_H
