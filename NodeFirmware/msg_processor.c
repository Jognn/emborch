/*
 * Copyright (C) 2022 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */


#include "msg_processor.h"

/** System */
#include <stdio.h>
#include <string.h>

/** Modules */
#include "periph/uart.h"
#include "isrpipe.h"
#include "cond.h"


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
uint8_t remainingMemory_kB = 20;


static inline MessageType getMessageType(uint8_t const firstMessageBlock)
{
    return ((firstMessageBlock & 0b11110000) >> 4) & 0b00001111;
}

static inline unsigned char createMessageHeader(MessageType const messageType)
{
    return ((messageType & 0b1111) << 4) | (assignedId & 0b1111);
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

static void send_message(void const *msg, int const msgLength)
{
    static uint8_t const etb = ETB_SIGN;
    uart_write(UART_USED, msg, msgLength);
    uart_write(UART_USED, &etb, 1);
}

static void interpretMessage(unsigned const numberOfBytes)
{
    MessageType const messageType = getMessageType(message[0]);
    switch (messageType)
    {
        case eMessageTypeRegister:
        {
            MessageRegister_Orchestrator const *msg = (MessageRegister_Orchestrator const *) &message[0];
            assignedId = msg->assignedId;
            printf("Assigned_id = %d\n", assignedId);
            break;
        }
        case eMessageTypeSendScript:
        {
            unsigned const scriptLength = numberOfBytes - sizeof(MessageHeader);
            remainingMemory_kB -= scriptLength;
            isrpipe_write(&luaPipe, message + sizeof(MessageHeader), scriptLength);
            cond_signal(&luaScriptReady);
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
    msg.messageHeader.messageType = createMessageHeader(eMessageTypeRegister);
    msg.messageHeader.senderId = INITIAL_ID;
    msg.availableMemory_kB = remainingMemory_kB;
    msg.supportedFeatures = 1 << 3; // DUMMY VALUE!!!
    send_message(&msg.bytes, sizeof(msg));
}

void msgp_pollMessages(void)
{
    puts("Sleeping...");
    cond_wait(&messageReceived, &uartPipe.mutex);

    puts("STOPPED SLEEPING!");
    unsigned const available = tsrb_avail(&uartPipe.tsrb);
    isrpipe_read(&uartPipe, message, available);
    interpretMessage(available);
}
