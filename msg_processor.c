//
// Created by jogn on 06.12.22.
//

#include "include/msg_processor.h"

#include "stdio.h"
#include "periph/uart.h"
#include "isrpipe.h"
#include "cond.h"
#include "string.h"

#define ETB_SIGN 23
#define LUA_SCRIPT_STANDARD_HEAP_REQUIRED 14

static isrpipe_t uartPipe;
static uint8_t uartPipeBuffer[BUFFER_SIZE];

static cond_t messageRecieved = COND_INIT;
static uint8_t message[BUFFER_SIZE];

isrpipe_t luaPipe;
uint8_t luaScript[BUFFER_SIZE];
cond_t luaScriptReady = COND_INIT;

uint8_t assigned_id = 0;
uint8_t available_memory = UINT8_MAX;


static inline MessageType getMessageType(uint8_t const firstMessageBlock)
{
    return ((firstMessageBlock & 0b11110000) >> 4) & 0b00001111;
}

static inline unsigned char createMessageHeader(MessageType const messageType)
{
    return ((messageType & 0b1111) << 4) | (assigned_id & 0b1111);
}

static void uart_cb(void *arg, uint8_t data)
{
    (void) arg;

    if(data == ETB_SIGN)
    {
        cond_signal(&messageRecieved);
    }
    else
    {
        isrpipe_write_one(&uartPipe, data);
    }
}

static void interpretMessage(unsigned const readBytes)
{
    MessageType const messageType = getMessageType(message[0]);
    switch (messageType)
    {
        case eMessageTypeRegister:
            assigned_id = message[1];
            printf("Assigned_id = %d\n", assigned_id);
            break;
        case eMessageTypeSendScript:
            available_memory -= LUA_SCRIPT_STANDARD_HEAP_REQUIRED;
            isrpipe_write(&luaPipe, message + 1, readBytes - 1);
            cond_signal(&luaScriptReady);
            break;
        default:
            printf("Provided message type %d is not supported\n", messageType);
            break;
    }
}

void msgp_init(void)
{
    isrpipe_init(&uartPipe, uartPipeBuffer, BUFFER_SIZE);
    isrpipe_init(&luaPipe, luaScript, BUFFER_SIZE);
    cond_init(&messageRecieved);
    uart_init(UART_DEV(0), 115200, uart_cb, NULL);
}

void msgp_checkUart(void)
{
    puts("Sleeping...");
    cond_wait(&messageRecieved, &uartPipe.mutex);

    puts("STOPPED SLEEPING!");
    unsigned available = tsrb_avail(&uartPipe.tsrb);
    isrpipe_read(&uartPipe, message, available);
    interpretMessage(available);
}

void msgp_register(void)
{
    unsigned char msg[3];
    msg[0] = createMessageHeader(eMessageTypeRegister);
    msg[1] = available_memory;
    msg[2] = ETB_SIGN;

    uart_write(UART_DEV(0), msg, sizeof(msg));
}
