import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
Mills = lambda: int(round(time.time() * 1000))
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c,address=0x49)
#ads.mode = 256
ads.mode = 256
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0, ADS.P1)
#chan1 = AnalogIn(ads, ADS.P1)
#chan2 = AnalogIn(ads, ADS.P2)
#chan3 = AnalogIn(ads, ADS.P3)

# Create single-ended input on channel 0


# The ADS1015 and ADS1115 both have the same gain options.
#
#       GAIN    RANGE (V)
#       ----    ---------
#        2/3    +/- 6.144
#          1    +/- 4.096
#          2    +/- 2.048
#          4    +/- 1.024
#          8    +/- 0.512
#         16    +/- 0.256
#
gains = (2 / 3, 1, 2, 4, 8, 16)

ads.gain = gains[1]

ads.data_rate = 860


FACTOR = 100
multiplier = 0.0485

def printMeasure (value):
    print("IRMS: {:>5.2f}".format(value))
    
def getCorriente():
    tiempo = Mills()
    rawAdc = chan.value
    minRaw = rawAdc
    maxRaw = rawAdc
    while (Mills() - tiempo < 1000):
        rawAdc = chan.value
        if maxRaw > rawAdc : 
            maxRaw = maxRaw
        else:
            maxRaw = rawAdc
            
        if minRaw > rawAdc : 
            minRaw = minRaw
        else:
            minRaw = rawAdc
    if maxRaw > -minRaw : 
        maxRaw = maxRaw
    else:
        maxRaw = -minRaw
    voltagePeak = maxRaw * multiplier / 1000
    voltageRMS = voltagePeak * 0.70710678118
    currentRMS = voltageRMS * FACTOR
    return currentRMS

#Ejecucion de bucle infinito
while True:
    currentRMS = getCorriente()
    power = 230.0 * currentRMS
    printMeasure(currentRMS)
    #print("DIFERENCIAL: {:>5.3f}".format(chan.voltage))
    time.sleep(0.1)