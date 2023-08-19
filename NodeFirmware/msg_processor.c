/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */


#include "msg_processor.h"
#include "messages.h"

/** System */
#include <stdio.h>
#include <string.h>

/** Modules */
#include "periph/uart.h"
#include "isrpipe.h"
#include "cond.h"
#include "lua_engine.h"
#include "definitons.h"


#define ETB_SIGN 23
#define UART_USED UART_DEV(0)


static isrpipe_t uartPipe;
static uint8_t uartPipeBuffer[BUFFER_SIZE];

static cond_t messageReceived = COND_INIT;
static uint8_t message[BUFFER_SIZE];

isrpipe_t luaPipe;
uint8_t luaPipeBuffer[BUFFER_SIZE];
cond_t luaScriptReady = COND_INIT;

uint8_t assignedId = 0;
uint8_t remainingMemory_kB = LUA_INTERPRETER_SIZE_B / 1000;


static inline MessageType getMessageType(uint8_t const firstMessageBlock)
{
    return ((firstMessageBlock & MESSAGE_TYPE_MASK) >> 4);
}

static inline MessageHeader createMessageHeader(MessageType const messageType)
{
    return (messageType << 4) | (assignedId & MESSAGE_SENDER_MASK);
}

static void uart_cb(void *arg, uint8_t data)
{
    (void) arg;

    if (data == ETB_SIGN)
    {
        cond_signal(&messageReceived);
    }
    else
    {
        isrpipe_write_one(&uartPipe, data);
    }
}

static void send_message(MessageType const messageType, void const *const msg, int const msgLength)
{
    static uint8_t const etb = ETB_SIGN;
    MessageHeader const messageHeader = createMessageHeader(messageType);

    uart_write(UART_USED, &messageHeader, sizeof(messageHeader));
    uart_write(UART_USED, msg, msgLength);
    uart_write(UART_USED, &etb, sizeof(etb));
}

static void interpretMessage(unsigned const numberOfBytes)
{
    MessageType const messageType = getMessageType(message[0]);
    switch (messageType)
    {
        case eMessageTypeRegister:
        {
            MessageRegister_Orchestrator const *msg = (MessageRegister_Orchestrator const *) &message[1];
            assignedId = msg->assignedId;
            printf("Assigned_id = %d\n", assignedId);
            break;
        }
        case eMessageTypeSendScript:
        {
            unsigned const scriptLength = numberOfBytes - sizeof(MessageHeader);
            remainingMemory_kB -= scriptLength;

            luae_shutdown();
            isrpipe_write(&luaPipe, message + sizeof(MessageHeader), scriptLength);
            cond_signal(&luaScriptReady);
            break;
        }
        case eMessageTypeMonitor:
        {
            puts("RESPONDING TO MONITOR REQUEST\n");
            uint8_t const currentLuaStatus = luae_getStatus();
            MessageMonitor_Node msg;
            msg.currentLuaStatus = currentLuaStatus;
            send_message(eMessageTypeMonitor, &msg.bytes, sizeof(msg));
            break;
        }
        default:
        {
            printf("Provided message type %d is not supported\n", messageType);
            break;
        }
    }
}

void msgp_init(void)
{
    isrpipe_init(&uartPipe, uartPipeBuffer, BUFFER_SIZE);
    isrpipe_init(&luaPipe, luaPipeBuffer, BUFFER_SIZE);

    cond_init(&messageReceived);
    uart_init(UART_USED, 115200, uart_cb, NULL);
}

void msgp_register(void)
{
    MessageRegister_Node msg;
    msg.availableMemory_kB = remainingMemory_kB;
    msg.supportedFeatures = FEATURE_BITSET;
    send_message(eMessageTypeRegister, &msg.bytes, sizeof(msg));
}

void msgp_pollMessages(void)
{
    puts("Sleeping...");
    cond_wait(&messageReceived, &uartPipe.mutex);

    puts("STOPPED SLEEPING!");
    unsigned const available = tsrb_avail(&uartPipe.tsrb);
    isrpipe_read(&uartPipe, message, available);
    interpretMessage(available);
    memset(&message[0], 0, available);
}
