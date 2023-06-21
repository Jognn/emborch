# Set the name of your application:
APPLICATION = emborch

# If no BOARD is found in the environment, use this default:
BOARD ?= nucleo-l476rg

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= $(RIOT)

# Uncomment this to enable scheduler statistics for ps:
# CFLAGS += -DSCHEDSTATISTICS

FEATURES_REQUIRED = periph_gpio

# Uncomment this to enable code in RIOT that does safety checking
# which is not needed in a production environment but helps in the
# development process:
DEVELHELP = 1
WERROR = 0

# Change this to 0 to show compiler invocation lines by default:
QUIET ?= 1

# Adding includes
INCLUDES += -I$(CURDIR)/include
INCLUDES += -DDEBUG_MODE=0
INCLUDES += -DNATIVE_TEST_MODE=0

# Adding the lua package
USEPKG += lua

# Modules to include:
USEMODULE += xtimer
USEMODULE += periph_gpio_irq
USEMODULE += periph_uart
USEMODULE += isrpipe

# Adding lua_enigne module directory
USEMODULE += lua_engine
EXTERNAL_MODULE_DIRS = $(CURDIR)

# generate .lua.h header files of .lua files
# BLOBS += $(wildcard *.lua)

include $(RIOTBASE)/Makefile.include
