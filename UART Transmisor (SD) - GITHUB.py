from machine import Pin, SPI
from sdcard import SDCard
from uos import VfsFat, mount
from os import listdir
import utime
import time

uart = machine.UART(0, baudrate=100000, tx=machine.Pin(0), rx=machine.Pin(1))

"""
#SPI
cs = Pin(5)
spi = SPI(1,
          baudrate=1000000,
          polarity=0,
          phase=0,
          sck = Pin(2),
          mosi = Pin(3),
          miso = Pin(4))
#SD
sd = SDCard(spi, cs)
vol = VfsFat(sd)
mount(vol, "/sd")

cont = 0
"""

def leer():
    try:
        with open('Alertas.txt', 'r') as file:
            lineas = file.readlines()
            datos = [linea.split(':')[-1].strip() for linea in lineas]  # Utiliza list comprehension para obtener los números
            return datos
    except FileNotFoundError:
        print("El archivo 'Alertas.txt' no se encontró.")
        return []  # Devuelve una lista vacía en caso de error
    except Exception as e:
        print("Ocurrió un error al intentar leer el archivo:", str(e))
        return []  # Devuelve una lista vacía en caso de error


alertas = leer()    
for alerta in alertas:
    uart.write(alerta)  # Escribir la alerta como una cadena de texto a través del UART
    print("Valor enviado: "+ str(alerta))
    utime.sleep_ms(100)