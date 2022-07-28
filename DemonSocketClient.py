import socket
import requests
import time
import json
from sensores.ZMPT101B import ZMPT101B
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

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
#Calibracion
calibraA = [0]*2
for i in range(10):
    c = ZMPT101B()
    calibraA[0]+=c.calibracion(chan)
    calibraA[1]+=c.calibracion(chan3)

#resp = requests.get('https://titulacion.sysnearnet.com/auth/api/login',params={'username': '1752349264', 'password': '1234'})
if 201 == 201:
    #resp = resp.json()
    #token = resp["token"]
    token = "36|BdJGfuW93NHB0B1JTyrb6fHzauakwuUyFuEUuPEp"
    while True:
        try:
            voltaje = ZMPT101B(140,26432,[chan,chan1,chan2,chan3],[calibraA[0]/10,13221.0,13221.0,calibraA[1]/10])
            v = voltaje.getVoltajeAC()
            resp = requests.get('https://titulacion.sysnearnet.com/evento',headers={'Authorization': 'Bearer '+token},params={'v1': v[0],'v2': v[1],'v3': v[2],'v4': v[3]})
            print (resp.text)
            if resp.status_code == 201:
                print (resp.json())
                #time.sleep(0.3)
        except:
            print ("ERROR")
            
    
#Ejecucion de bucle infinito

    #try:
        #mi_socket = socket.socket()
        #mi_socket.connect(('144.126.143.111', 5478))

        
        #SData = json.dumps({"V1": int(v[0]), "V2": int(v[3]), "A1":50, "A2":100})
        #byt = SData.encode()
        #mi_socket.send(byt)
        #-----------------------------------------------
        #resp = mi_socket.recv(1024)
        #print (resp)
        #st='Hola desde el cliente \n'
        #byt=st.encode()
            #mi_socket.send(byt);
        #mi_socket.close()
        #time.sleep(0.3)
    #except:
    #    if mi_socket is not None:
    #        mi_socket.close()