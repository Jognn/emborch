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

static isrpipe_t uartPipe;
static uint8_t uartPipeBuffer[BUFFER_SIZE];

static cond_t messageRecieved = COND_INIT;
static uint8_t message[BUFFER_SIZE];

isrpipe_t luaPipe;
uint8_t luaScript[BUFFER_SIZE];
cond_t luaScriptReady = COND_INIT;


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

static inline MessageType getMessageType(uint8_t const firstMessageBlock)
{
    return ((firstMessageBlock & 0b11110000) >> 4) & 0b00001111;
}

static void interpretMessage(unsigned const readBytes)
{
    MessageType const messageType = getMessageType(message[0]);
    switch (messageType)
    {
        case eMessageTypeRegister:

        case eMessageTypeSendScript:
            isrpipe_write(&luaPipe, message+1, readBytes-1);
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
    RegisterMessage registerMessage = {
            .messageType = eMessageTypeRegister,
            .message_sender = 0,
            .available_memory = 100,
    };

    char msg[3];
    msg[0] = 0x00;
    msg[1] = 100;
    msg[2] = ETB_SIGN;

//    for(unsigned i = 0; i < 3; ++i)
//    {
//        char temp[2];
//        temp[0] = msg[i];
//        temp[1] = '\0';
//        puts(temp);
//    }

    uart_write(UART_DEV(0), msg, sizeof(msg));
}
