import time
import math

class ZMPT101B:
    # VoltajeRef = voltaje referencial maximo a medir caso 250
    # ResolucionAnalogica = resolucion del sensor analogico
    # AnalogoInput = [A0,A1,A2,A3] entradas analogicas
    # CalibracionVoltaje0 = [v1,v2,v3,v4] valor de entradas analogicas cuando voltaje es 0
    def __init__(self, VoltajeRef, ResolucionAnalogica, AnalogoInput, CalibracionVoltaje0):
        self.__NFrecuencia = 60
        self.__Micros = lambda: int(round(time.time() * 10000000))
        self.__Muestra = [0]*4
        self.__VoltajeRef = VoltajeRef
        self.__Sensivilidad = 0.029
        self.__ResolucionAnalogica = ResolucionAnalogica
        self.__CalibracionVoltaje0 = CalibracionVoltaje0  # ads1115 16 bits v0 = CalibracionVoltaje0
        self.__AnalogoInput = AnalogoInput

    def getVoltajeAC(self):
            periodo = 1000000 / self.__NFrecuencia
            time_start = self.__Micros()
            VoltajeSuma = [0]*4
            preiodo_contador = 0
            VoltajeActual = [0]*4
            while (self.__Micros() - time_start < periodo):
                VoltajeActual[0] = self.__AnalogoInput[0].value-self.__CalibracionVoltaje0[0]
                VoltajeActual[1] = self.__AnalogoInput[1].value-self.__CalibracionVoltaje0[1]
                VoltajeActual[2] = self.__AnalogoInput[2].value-self.__CalibracionVoltaje0[2]
                VoltajeActual[3] = self.__AnalogoInput[3].value-self.__CalibracionVoltaje0[3]

                VoltajeSuma[0] += VoltajeActual[0]*VoltajeActual[0]
                VoltajeSuma[1] += VoltajeActual[1]*VoltajeActual[1]
                VoltajeSuma[2] += VoltajeActual[2]*VoltajeActual[2]
                VoltajeSuma[3] += VoltajeActual[3]*VoltajeActual[3]

                preiodo_contador=preiodo_contador+1

            self.__Muestra[0] = (math.sqrt(VoltajeSuma[0] / preiodo_contador) * self.__VoltajeRef) / self.__ResolucionAnalogica
            self.__Muestra[1] = (math.sqrt(VoltajeSuma[1] / preiodo_contador) * self.__VoltajeRef) / self.__ResolucionAnalogica
            self.__Muestra[2] = (math.sqrt(VoltajeSuma[2] / preiodo_contador) * self.__VoltajeRef) / self.__ResolucionAnalogica
            self.__Muestra[3] = (math.sqrt(VoltajeSuma[3] / preiodo_contador) * self.__VoltajeRef) / self.__ResolucionAnalogica
            
        return self.__Muestra
