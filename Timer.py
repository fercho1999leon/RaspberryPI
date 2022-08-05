import threading
from functools import wraps
def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap

class Timer():
    # FLAG MIENTRAS SE ESTA EJECUTANDO ES FALSO, SE CANCELA O SE COMPLETA LA TAREA REGRESA A TRUE
    toClearTimer = False
    def __init__(self):
        self.__flag = True
    def setTimeout(self, fn, time):
        self.__flag = False
        isInvokationCancelled = False
        @delay(time)
        def some_fn():
                if (self.toClearTimer is False):
                        fn()
                        self.__flag = True
                else:
                    print('Invokation is cleared!')
                    self.__flag = True 
        some_fn()
        return isInvokationCancelled
    def setClearTimer(self):
        self.toClearTimer = True
    def getFlag(self):
        return self.__flag