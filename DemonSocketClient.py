import requests
from multiprocessing.pool import ThreadPool
from sensores.ZMPT101B import ZMPT101B
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from Timer import Timer
from adafruit_ads1x15.analog_in import AnalogIn
from sensores.SCT013100 import SCT013100
import RPi.GPIO as GPIO
import time

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
InputAmper2 = AnalogIn(adsAmper, ADS.P2, ADS.P3)

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

token = "6|BPOnoIZzD9feD21vFVDCqqEx7uRJm7WgCg7abZcM"
#TITULACION 6|BPOnoIZzD9feD21vFVDCqqEx7uRJm7WgCg7abZcM
#LOCAL 1|gZdi85H8sqjbjE5XDdeBuz8C1frboBcZVeZGKtWn
urlApi = "titulacion.sysnearnet.com"
protocoloApi = "https"
csrf = None
config_line = None
config_timeActionError = None
config_timeLastError = None
config_email = None
config_vmax = None
config_vmin = None
V = None
A = None

#CONFIGURACION PARA RELE
print (GPIO.getmode())
PIN = 6
GPIO.setup(PIN, GPIO.OUT)

timer_exec_v_error = Timer()
flag_arranque_motor = False

def exec_v_error():
    if V[0]<config_vmin or V[0]>config_vmax:
        print('ARRANQUE')
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(8)
        print('PARE')
        GPIO.output(PIN, GPIO.LOW)


config = requests.get(protocoloApi+'://'+urlApi+'/api/getconfig',headers={'Authorization': 'Bearer '+token})
if config.status_code == 200:
    print (config.text)
    config = config.json()
    csrf = (config[0])['CSRF_TOKEN']
    config_line = ((config[0])["CONFIG"])["line"]
    config_timeActionError = ((config[0])["CONFIG"])["timeActionError"]
    config_timeLastError = ((config[0])["CONFIG"])["timeLastError"]
    config_email = ((config[0])["CONFIG"])["email"]
    config_vmax = ((config[0])["CONFIG"])["vmax"]
    config_vmin = ((config[0])["CONFIG"])["vmin"]

if 201 == 201:
    #resp = resp.json()
    #token = resp["token"]
    while True:
        try:
            pool_voltaje = ThreadPool(processes=1)
            pool_corriente = ThreadPool(processes=1)
            voltaje = ZMPT101B(150,32767,[InputVoltage,InputVoltage3],[calibraA[0]/10,calibraA[1]/10])
            corriente = SCT013100(100,0.0485,[InputAmper,InputAmper2],1000)
            async_voltage = pool_voltaje.apply_async(voltaje.getVoltajeAC)
            async_corriente = pool_voltaje.apply_async(corriente.getArrayCurrent)
            V = async_voltage.get()
            A = async_corriente.get()
            if V[0]<config_vmin or V[0]>config_vmax:
                if timer_exec_v_error.getFlag():
                    requests.get(protocoloApi+'://'+urlApi+'/send/correo',headers={'Authorization': 'Bearer '+token},params={'v1':V[0],'vmin':config_vmin,'vmax':config_vmax,'timeActionError':config_timeActionError,'email':config_email})
                    timer_exec_v_error.setTimeout(exec_v_error, 60*config_timeActionError)
                    
            resp = requests.get(protocoloApi+'://'+urlApi+'/event/dashboard',headers={'Authorization': 'Bearer '+token},params={'v1': V[0],'v2': V[1],'a1': A[0],'a2': A[1]})
            if resp.status_code == 201:
                print (resp.json())
                print("v1: {:>5.2f}\t v2: {:>5.2f}\t a1: {:>5.2f}\t a2: {:>5.2f}".format(V[0],V[1],A[0],A[1]))
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