#! /usr/bin/python

# A simple Python command line tool to control an MCP23008 I2C IO Expander
# for Python 2 and 3 that can also be imported and used as a class.

# By Andrew Thomas 2020 (https://github.com/drandrewthomas).

# Concept and code based on:

# A simple Python command line tool to control an MCP23017 I2C IO Expander
# By Nathan Chantrell http://nathan.chantrell.net

import smbus
import sys
import getopt


class mcp23008:

    def __init__(self):
        self.busnum=1
        self.addr=0x20
        self.i2cbus=-1
        self.LOW=0
        self.HIGH=1
        self.INPUT=1
        self.OUTPUT=0
        self.DISABLE=0
        self.ENABLE=1

    def begin(self):
        self.i2cbus=smbus.SMBus(self.busnum)

    def bus(self):
        return self.i2cbus

    def set_bus(self,b):
        if self.i2cbus!=-1:
            print("MCP23008 error: Bus number cannot be set after calling begin()!")
            sys.exit(2)
        self.busnum=b

    def address(self):
        return self.addr

    def set_address(self,add):
        if self.i2cbus!=-1:
            print("MCP23008 error: Address cannot be set after calling begin()!")
            sys.exit(2)
        self.addr=add

    def directions(self):
        dirs=self.i2cbus.read_byte_data(self.addr,0x00)
        return dirs

    def direction(self,pin):
        if pin<0 or pin>7:
            print("MCP23008 error: Pin numbers must be between 0 and 7!")
            sys.exit(2)
        return (self.directions() >> pin) & 1 
 
    def set_directions(self,dirs):
        if self.i2cbus==-1:
            print("MCP23008 error: Directions can only be set after calling begin()!")
            sys.exit(2)
        self.i2cbus.write_byte_data(self.addr,0x00,dirs)

    def set_direction(self,pin,pdir):
        if self.i2cbus==-1:
            print("MCP23008 error: Directions can only be set after calling begin()!")
            sys.exit(2)
        if pin<0 or pin>7:
            print("MCP23008 error: Pin numbers must be between 0 and 7!")
            sys.exit(2)
        if pdir!=0 and pdir!=1:
            print("MCP23008 error: Pin directions must be either 0 or 1!")
            sys.exit(2)
        if self.direction(pin)==pdir: return
        if pdir==0: # output
            d=self.directions()-(1<<pin)
        elif pdir==1: # input
            d=self.directions()+(1<<pin)
        else:
            print("MCP23008 error: Pin directions must be 0 or 1!")
            sys.exit(2)
        self.set_directions(d)

    def gpio(self,pin=-1):
        if self.i2cbus==-1:
            print("MCP23008 error: GPIO values can only be queried after calling begin()!")
            sys.exit(2)
        if pin>7:
            print("MCP23008 error: Pin numbers must be between 0 and 7!")
            sys.exit(2)
        gpio=self.i2cbus.read_byte_data(self.addr,0x09)
        if pin!=-1:
            gpio=(gpio >> pin) & 1 
        return gpio

    def set_gpio(self,pin,gpio):
        if self.i2cbus==-1:
            print("MCP23008 error: GPIO values can only be set after calling begin()!")
            sys.exit(2)
        if pin<0 or pin>7:
            print("MCP23008 error: Pin numbers must be between 0 and 7!")
            sys.exit(2)
        if gpio!=0 and gpio!=1:
            print("MCP23008 error: Pins can only be set to 0 or 1!")
            sys.exit(2)
        gp=self.gpio()
        if ((gp >> pin) & 1)==1:
            gp-=(1 << pin)
        gp+=(gpio << pin)
        self.i2cbus.write_byte_data(self.addr,0x09,gp)

    def pullups(self,pin=-1):
        if self.i2cbus==-1:
            print("MCP23008 error: Pin pullup values can only be queried after calling begin()!")
            sys.exit(2)
        if pin>7:
            print("MCP23008 error: Pin numbers must be between 0 and 7!")
            sys.exit(2)
        pups=self.i2cbus.read_byte_data(self.addr,0x06)
        if pin!=-1:
            pups=(pups >> pin) & 1 
        return pups

    def set_pullup(self,pin,pups):
        if self.i2cbus==-1:
            print("MCP23008 error: Pin pullup values can only be set after calling begin()!")
            sys.exit(2)
        if pin<0 or pin>7:
            print("MCP23008 error: Pin numbers must be between 0 and 7!")
            sys.exit(2)
        if pups!=0 and pups!=1:
            print("MCP23008 error: Pin pullups can only be set to 0 or 1!")
            sys.exit(2)
        pu=self.pullups()
        if((pu >> pin) & 1)==1:
            pu-=(1 << pin)
        pu+=(pups << pin)
        self.i2cbus.write_byte_data(self.addr,0x06,pu)


# Let them know how it works
def usage():
    print("Usage: mcp23008.py -b <i2cbus> -a <i2caddress> -o <output pin> -s <high|low>")
    print("\t-b (optional) : Bus number should be 0 for old Pi's or 1 for newer Pi's (default is 1)")
    print("\t-a (optional) : Address should be 0 for 0x20, 1 for 0x21, etc. (default is 0 for 0x21)")
    print("\t-o (required) : GPIO pin number that is to have its state set (0 to 7)")
    print("\t-s (required) : State the GPIO pin is to be set to (either 'high' or 'low')")

# Handle the command line arguments
def main():
    mcp=mcp23008()
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hb:a:o:s:",["bus=","address=","output=","state="])
        if not opts:
            usage()
            sys.exit(2)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    gotoutput=False
    gotstate=False
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-a", "--address"):
            mcp.set_address(0x20+int(arg))
        elif opt in ("-b", "--bus"):
            mcp.set_bus(int(arg))
        elif opt in ("-o", "--output"):
            output=int(arg)
            gotoutput=True
        elif opt in ("-s", "--state"):
            state=-1
            if arg=="low" or arg=="0":
                state=0
            elif arg=="high" or arg=="1":
                state=1
            else:
                print("MCP23008 error: State must be either 'low' or 'high' (or use 0 or 1)!")
                sys.exit(2)
            gotstate=True
    if not gotoutput or not gotstate:
        print("MCP23008 error: Output pin and state must both be specified!")
        sys.exit(2)
    mcp.begin()
    mcp.set_direction(output,0)
    mcp.set_gpio(output,state)
    print("Output "+str(output)+" changed to "+["low (0)","high (1)"][state])

if __name__ == "__main__":
    main()
