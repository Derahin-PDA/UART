import machine
import ssd1306
import time

# Inicializar componentes
uart = machine.UART(0, baudrate=100000, tx=machine.Pin(0), rx=machine.Pin(1))
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

# Variables globales
ciclo = 2
tiempo = time.time()
lista = []

# Función para graficar
def formato_grafica(alertas):
    global tiempo, lista, X_prev, Y_prev  # Declarar variables globales

    # Limpiar la pantalla OLED
    oled.fill(0)

    # Obtener la fecha y hora actuales
    current_time = time.localtime()
    template_fecha = "{:02d}/{:02d}/{:04d}".format(current_time[2], current_time[1], current_time[0])
    template_hora = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])

    # Mostrar la fecha y hora en la pantalla OLED
    oled.text(template_fecha, 0, 0)
    oled.text(template_hora, 0, 9)
    oled.hline(0, 16, 128, 1)  # Línea divisoria

    # Verificar si es tiempo de actualizar la lista y la gráfica
    #if tiempo + ciclo < time.time():
    lista.insert(0, alertas)  # Agregar alerta a la lista
    tiempo = time.time()  # Actualizar el tiempo
    for k in range(len(lista)):
        X = 132 - (k + 1) * 8
        Y = int(60 - lista[k] * 5) if tiempo + ciclo < time.time() else int(60 - lista[k])
        oled.pixel(X, Y, 1)  # Dibujar píxel en la pantalla OLED
        if k > 0:
            oled.line(X_prev, Y_prev, X, Y, 1)  # Dibujar línea entre píxeles
        X_prev, Y_prev = X, Y

    oled.show()  # Mostrar cambios en la pantalla OLED

# Bucle principal
while True:
    if uart.any():
        data = uart.read()  # Leer los bytes del UART
        alert = int(data.decode('utf-8'))  # Convertir los datos leídos a entero
        formato_grafica(alert)  # Llamar a formato_grafica() con 'alert' como argumento
        print("Mensaje recibido:", alert)