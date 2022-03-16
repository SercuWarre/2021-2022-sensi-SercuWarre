from serial import Serial, PARITY_NONE 
 
# simple echo server 
with Serial('/dev/ttyS0', 115200, bytesize=8, parity=PARITY_NONE, stopbits=1) as 
port: 
    while True: 
        line = port.readline() 
        port.write(line)
