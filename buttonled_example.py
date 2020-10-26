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
