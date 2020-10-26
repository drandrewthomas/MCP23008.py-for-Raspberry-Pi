from time import sleep
import mcp23008 as mcp

ledpin=7

dev=mcp.mcp23008()
dev.set_address(0x20)
dev.set_bus(1)
dev.begin()
dev.set_direction(ledpin,dev.OUTPUT)
while 1:
    dev.set_gpio(ledpin,dev.HIGH)
    sleep(0.5)
    dev.set_gpio(ledpin,dev.LOW)
    sleep(2)
