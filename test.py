# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

micros = lambda: int(round(time.time() * 10000000))
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
#ads.mode = 256
ads.mode = 256
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

#variables
sensorValue1 = 0
sensorValue2 = 0
crosscount = 0
climb_flag = 0
val =0
max_v = 0
VmaxD = 0
VeffD = 0
Veff = 0

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

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

print("{:>5}\t{:>5}\t{:>5}\t{:>5}".format("A0", "A1", "A2", "A3"))
print("-"*20)

cont = 0

muestra = 0

ads.data_rate = 860

periodo = 100000000 / 50
t_start = micros()
Vsum = 0
measurements_count = 0
Vnow = 0
while (micros() - t_start < periodo):
    Vnow = chan.value
    Vsum = Vsum + Vnow
    measurements_count=measurements_count+1
val = Vsum / measurements_count
print (val)
    

#while cont < 60:
    #muestra[0] = muestra[0] + chan.value
    #muestra[1] = muestra[1] + chan1.value
    #muestra[2] = muestra[2] + chan2.value
#    muestra[3] = muestra[3] + chan3.value
#    cont = cont+1
    #print("{:>5.3f}\t{:>5.3f}\t{:>5.3f}\t{:>5.3f}".format(muestra[0],muestra[1],muestra[2],muestra[3]))
    #print("{:>5.3f}\t{:>5.3f}\t{:>5.3f}\t{:>5.3f}".format(chan.value,chan1.value,chan3.value,chan3.voltage))
    #time.sleep(0.05)
#muestra[0] = muestra[0] / 1000
#muestra[1] = muestra[1] / 1000
#muestra[2] = muestra[2] / 1000
#muestra[3] = muestra[3] / 60
#muestra[3] = (muestra[3]*3.3)/26432
#print("{:>5.3f}".format(muestra[3]))
#print("{:>5.3f}\t{:>5.3f}\t{:>5.3f}\t{:>5.3f}".format(muestra[0],muestra[1],muestra[2],muestra[3]))
