# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 7 – Semaforo con interfaz grafica y boton
#
#  Descripcion general:
#  Este programa extiende el Ejercicio 6 agregando una interfaz grafica
#  utilizando Tkinter.
#
#  El sistema mantiene exactamente la misma logica:
#
#      VERDE ----(boton)----> AMARILLO → ROJO → VERDE
#
#  Caracteristicas del sistema:
#
#   - Control GPIO de LEDs
#   - Interrupcion por boton
#   - Eliminacion de rebotes
#   - Maquina de estados
#   - Visualizacion grafica del sistema
#
# =====================================================================================


# -------------------------------------------------------------------------------------
# Importacion de librerias
# -------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import tkinter as tk
import time


# -------------------------------------------------------------------------------------
# Definicion de pines
# -------------------------------------------------------------------------------------

pin_rojo = 17
pin_amarillo = 27
pin_verde = 22

pin_boton = 23


# -------------------------------------------------------------------------------------
# Definicion de tiempos (segundos)
# -------------------------------------------------------------------------------------

tiempo_verde = 5
tiempo_amarillo = 2
tiempo_rojo = 5

tiempo_debounce = 0.2


# -------------------------------------------------------------------------------------
# Configuracion GPIO
# -------------------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_verde, GPIO.OUT)
GPIO.setup(pin_amarillo, GPIO.OUT)
GPIO.setup(pin_rojo, GPIO.OUT)

GPIO.setup(pin_boton, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# -------------------------------------------------------------------------------------
# Variables del sistema
# -------------------------------------------------------------------------------------

estado_actual = "VERDE"

solicitud_peaton = False

ultimo_evento = 0

inicio_estado = time.time()


# -------------------------------------------------------------------------------------
# Rutina de interrupcion del boton
# -------------------------------------------------------------------------------------

def ISR_boton(channel):

    global solicitud_peaton
    global ultimo_evento
    global estado_actual

    tiempo_actual = time.time()

    if tiempo_actual - ultimo_evento > tiempo_debounce:

        if estado_actual == "VERDE":

            solicitud_peaton = True
            mensaje.set("Peaton detectado")

            canvas.itemconfig(indicador_boton, fill="blue")

            print("Interrupcion: solicitud de peaton")

        ultimo_evento = tiempo_actual


GPIO.add_event_detect(
    pin_boton,
    GPIO.FALLING,
    callback=ISR_boton
)


# -------------------------------------------------------------------------------------
# Funcion de actualizacion del sistema (maquina de estados)
# -------------------------------------------------------------------------------------

def actualizar_sistema():

    global estado_actual
    global solicitud_peaton
    global inicio_estado

    tiempo_actual = time.time()


    # =====================================================
    # ESTADO VERDE
    # =====================================================

    if estado_actual == "VERDE":

        GPIO.output(pin_verde, GPIO.HIGH)
        GPIO.output(pin_amarillo, GPIO.LOW)
        GPIO.output(pin_rojo, GPIO.LOW)

        canvas.itemconfig(led_verde, fill="green")
        canvas.itemconfig(led_amarillo, fill="gray")
        canvas.itemconfig(led_rojo, fill="gray")

        if solicitud_peaton:

            solicitud_peaton = False
            estado_actual = "AMARILLO"
            inicio_estado = tiempo_actual
            print("Cambio a AMARILLO")

        elif tiempo_actual - inicio_estado >= tiempo_verde:

            estado_actual = "AMARILLO"
            inicio_estado = tiempo_actual
            print("Cambio a AMARILLO")


    # =====================================================
    # ESTADO AMARILLO
    # =====================================================

    elif estado_actual == "AMARILLO":

        GPIO.output(pin_verde, GPIO.LOW)
        GPIO.output(pin_amarillo, GPIO.HIGH)
        GPIO.output(pin_rojo, GPIO.LOW)

        canvas.itemconfig(led_verde, fill="gray")
        canvas.itemconfig(led_amarillo, fill="yellow")
        canvas.itemconfig(led_rojo, fill="gray")

        if tiempo_actual - inicio_estado >= tiempo_amarillo:

            estado_actual = "ROJO"
            inicio_estado = tiempo_actual
            print("Cambio a ROJO")


    # =====================================================
    # ESTADO ROJO
    # =====================================================

    elif estado_actual == "ROJO":

        GPIO.output(pin_verde, GPIO.LOW)
        GPIO.output(pin_amarillo, GPIO.LOW)
        GPIO.output(pin_rojo, GPIO.HIGH)

        canvas.itemconfig(led_verde, fill="gray")
        canvas.itemconfig(led_amarillo, fill="gray")
        canvas.itemconfig(led_rojo, fill="red")

        if tiempo_actual - inicio_estado >= tiempo_rojo:

            estado_actual = "VERDE"
            inicio_estado = tiempo_actual

            canvas.itemconfig(indicador_boton, fill="gray")

            mensaje.set("Sistema en funcionamiento")

            print("Cambio a VERDE")


    ventana.after(50, actualizar_sistema)


# -------------------------------------------------------------------------------------
# Creacion de interfaz grafica
# -------------------------------------------------------------------------------------

ventana = tk.Tk()

ventana.title("Sys On Chip - Semaforo Inteligente")

canvas = tk.Canvas(ventana, width=220, height=420)

canvas.pack()


# LEDs del semaforo

led_rojo = canvas.create_oval(70, 40, 150, 120, fill="gray")

led_amarillo = canvas.create_oval(70, 150, 150, 230, fill="gray")

led_verde = canvas.create_oval(70, 260, 150, 340, fill="gray")


# Indicador del boton

canvas.create_text(110, 360, text="Boton")

indicador_boton = canvas.create_oval(95, 370, 125, 400, fill="gray")


# Mensaje del sistema

mensaje = tk.StringVar()

mensaje.set("Sistema iniciado")

label_mensaje = tk.Label(ventana, textvariable=mensaje)

label_mensaje.pack()


# -------------------------------------------------------------------------------------
# Inicio del sistema
# -------------------------------------------------------------------------------------

print("Sistema iniciado")

inicio_estado = time.time()

ventana.after(50, actualizar_sistema)


# -------------------------------------------------------------------------------------
# Ejecucion del sistema
# -------------------------------------------------------------------------------------

try:

    ventana.mainloop()

finally:

    GPIO.cleanup()

    print("GPIO liberado correctamente")
