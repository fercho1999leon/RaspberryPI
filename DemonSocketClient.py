from re import A
import requests
from multiprocessing.pool import ThreadPool
from sensores.ZMPT101B import ZMPT101B
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from sensores.SCT013100 import SCT013100

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
adsVoltage = ADS.ADS1115(i2c)
adsAmper = ADS.ADS1115(i2c,address=0x49)
#ads.mode = 256
adsVoltage.mode = 256
adsAmper.mode = 256
# Create single-ended input on channel 0
InputVoltage = AnalogIn(adsVoltage, ADS.P0)
InputVoltage3 = AnalogIn(adsVoltage, ADS.P3)

InputAmper = AnalogIn(adsAmper, ADS.P0, ADS.P1)

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
adsVoltage.gain = gains[1]
adsAmper.gain = gains[1]
adsVoltage.data_rate = 860
adsAmper.data_rate = 860
#Calibracion
calibraA = [0]*2
for i in range(10):
    c = ZMPT101B()
    calibraA[0]+=c.calibracion(InputVoltage)
    calibraA[1]+=c.calibracion(InputVoltage3) 
#resp = requests.get('https://titulacion.sysnearnet.com/auth/api/login',params={'username': '1752349264', 'password': '1234'})
if 201 == 201:
    #resp = resp.json()
    #token = resp["token"]
    token = "1|jvX8xPmkCN623vXRFS8j7zCox6aNr7OoIILsyiig"
    while True:
        try:
            pool_voltaje = ThreadPool(processes=1)
            pool_corriente = ThreadPool(processes=1)
            voltaje = ZMPT101B(150,32767,[InputVoltage,InputVoltage3],[calibraA[0]/10,calibraA[1]/10])
            corriente = SCT013100(100,0.0485,InputAmper,1000)
            async_voltage = pool_voltaje.apply_async(voltaje.getVoltajeAC)
            async_corriente = pool_voltaje.apply_async(corriente.getCorriente)
            V = async_voltage.get()
            A = async_corriente.get()
            #print("v1: {:>5.2f}\t v2: {:>5.2f}\t a1: {:>5.2f}\t a2".format(V[0],V[1],A,0))
            resp = requests.get('https://titulacion.sysnearnet.com/evento',headers={'Authorization': 'Bearer '+token},params={'v1': V[0],'v2': V[1],'a1': A,'a2': 0})
            if resp.status_code == 201:
                print (resp.json())
                print("v1: {:>5.2f}\t v2: {:>5.2f}\t a1: {:>5.2f}\t a2".format(V[0],V[1],A,0))
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