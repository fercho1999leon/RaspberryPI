import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from sensores.ZMPT101B import ZMPT101B

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
#ads.mode = 256
ads.mode = 256
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)
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
calibraA = [0]*2
for i in range(10):
    c = ZMPT101B()
    calibraA[0]+=c.calibracion(chan)
    calibraA[1]+=c.calibracion(chan3)
print(calibraA[1]/10)
print(calibraA[0]/10)

#Ejecucion de bucle infinito
while True:
    voltaje = ZMPT101B(140,26432,[chan,chan1,chan2,chan3],[calibraA[0]/10,13221.0,13221.0,calibraA[1]/10])
    v = voltaje.getVoltajeAC()
    print("v1: {:>5.3f}\tv2: {:>5.3f}".format(v[0],v[3]))