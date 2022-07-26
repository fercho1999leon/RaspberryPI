# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math

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
#chan = AnalogIn(ads, ADS.P0)
#chan1 = AnalogIn(ads, ADS.P1)
#chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

#Calibration

#variables
muestra =[0]*100
voltaje_max = 0

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

while True:
    for i in range(60):
        periodo = 10000000 / 60
        t_start = micros()
        Vsum = 0
        measurements_count = 0
        Vnow = 0
        while (micros() - t_start < periodo):
            Vnow = chan3.value-13221.0
            Vsum += Vnow*Vnow
            measurements_count=measurements_count+1
        muestra[i] = math.sqrt(Vsum / measurements_count) / 26432 * 250 / 0.029
    voltaje_max = 0
    for i in range(60):
        if muestra[i] > voltaje_max:
            voltaje_max = muestra[i]
        muestra[i] = 0
    if voltaje_max < 10:
        print ("Voltaje = {:>5.1f}".format(0))
    else:
        print ("Voltaje = {:>5.1f}".format(voltaje_max))