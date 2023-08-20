/*
 * Copyright (C) 2023 Jognn
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#include <stdint.h>


/** Initialize the Lua Engine */
void luae_init(void);

/** Immediately shutdowns the Lua interpreter */
void luae_shutdown(void);

/** Retrieve the current Lua Engine's state */
uint8_t luae_getStatus(void);