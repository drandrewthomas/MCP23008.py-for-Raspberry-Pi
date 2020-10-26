from time import sleep
import mcp23008 as mcp

buttonpin=6
dev=mcp.mcp23008()
dev.set_address(0x20)
dev.set_bus(1)
dev.begin()
dev.set_direction(buttonpin,dev.INPUT)
dev.set_pullup(buttonpin,dev.ENABLE)
sleep(0.5)
lastbut=1-dev.gpio(buttonpin)
while 1:
    but=1-dev.gpio(buttonpin)
    if but!=lastbut:
        if but==dev.LOW:
            print("Button released.")
        elif but==dev.HIGH:
            print("Button pressed.")
    lastbut=but
    sleep(0.1)
