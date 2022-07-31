import time

class SCT013100:
    def __init__ (self,Amax=100,Multiplicador=0.0485,InputA=None,Range=1000):
        self.__Amax = Amax
        self.__Multiplicador = Multiplicador
        self.__Mills = lambda: int(round(time.time() * Range))
        self.__InputA = InputA
        self.__Range = Range
        self.__Sensivity = 0.70710678118
    
    def getCorriente(self):
        if self.__InputA!= None:
            tiempo = self.__Mills()
            rawAdc = self.__InputA.value
            minRaw = rawAdc
            maxRaw = rawAdc
            while (self.__Mills() - tiempo < self.__Range):
                rawAdc = self.__InputA.value
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
            voltagePeak = maxRaw * self.__Multiplicador / self.__Range
            voltageRMS = voltagePeak * self.__Sensivity
            currentRMS = voltageRMS * self.__Amax
            return currentRMS
        return 0