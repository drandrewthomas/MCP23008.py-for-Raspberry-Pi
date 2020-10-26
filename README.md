# MCP23008.py for Raspberry Pi

## What is MCP23008.py?

MCP23008.py is a Python (2 or 3) commandline tool and library for the MCP23008 I2C I/O expander chip. It's intended for use on a Raspberry Pi but should work with (or be easily ported to) similar single board Linux computers.

## Commandline usage

Below is the basic format for use on the commandline. If you're using Python 3 just change the start to python3 and it will still work exactly the same.

***python mcp23008.py -b &lt;i2cbus&gt; -a &lt;i2caddress&gt; -o &lt;output pin&gt; -s &lt;high|low&gt;***

Each of the options can be set as detailed below:

-b (optional) : Bus number should be 0 for old Pi's or 1 for newer Pi's (default is 1).

-a (optional) : Address should be 0 for 0x20, 1 for 0x21, etc. (default is 0 for 0x21).

-o (required) : GPIO pin number that is to have its state set (0 to 7).

-s (required) : State the GPIO pin is to be set to (either 'high' or 'low').

If you regularly need to include the address or bus parameters you can, of course, edit mcp23008.py to change the default values near the top of the file.

## Importing into your own Python code

Three examples are included that illustrate use of mcp23008.py in your own programs as a library (the pins to connect the LED and/or pull-down switch to are shown in the example codes). However, here's the button and LED example as a quick illustration of how it works:

```
from time import sleep
import mcp23008 as mcp

buttonpin=6
ledpin=7

dev=mcp.mcp23008()
dev.set_address(0x20)
dev.set_bus(1)
dev.begin()
dev.set_direction(ledpin,dev.OUTPUT)
dev.set_direction(buttonpin,dev.INPUT)
dev.set_pullup(buttonpin,dev.ENABLE)
sleep(0.5)
while 1:
    but=1-dev.gpio(buttonpin)
    dev.set_gpio(ledpin,but)
    sleep(0.1)
```

## Acknowledgements

The original concept and code was based on MCP23017.py by Nathan Chantrell [on his Github](http://nathan.chantrell.net). In the end most of his code has gone, and some bugs removed, in changing the code to a class base and for use with Python 2 or 3. However, it was a great inspiration to code a similar tool for the MCP23008 and so is gratefully acknowledged.
