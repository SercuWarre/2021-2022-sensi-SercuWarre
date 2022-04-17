import spidev
spi = spidev.SpiDev()
class MCPclass:
    def __init__(self,bus=0,device=0):
        global spi
        spi.open(bus,device)
        spi.max_speed_hz = 10 ** 5

    def read_channel(self,ch):
        spidata = spi.xfer2([1,(8|ch)<<4,0])
        return spidata

    def closespi(self):
        global spi
        spi.close()