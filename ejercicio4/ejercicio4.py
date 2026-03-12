# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 4 – Semaforo con interfaz grafica (Tkinter)
#
#  Descripcion general:
#  Este programa extiende el Ejercicio No.2 agregando una interfaz grafica
#  que permite visualizar el estado del semaforo controlado por la
#  Raspberry Pi.
#
#  El sistema controla tres LEDs fisicos conectados a los pines GPIO
#  y al mismo tiempo muestra tres LEDs virtuales en una ventana grafica.
#
#  Cada LED virtual representa una luz del semaforo:
#
#      Verde
#      Amarillo
#      Rojo
#
#  En este ejercicio aprenderemos:
#
#   1) Como representar multiples LEDs virtuales usando Tkinter.
#   2) Como sincronizar hardware GPIO con una interfaz grafica.
#   3) Como crear animaciones temporizadas usando el metodo after().
#   4) Como implementar una secuencia de estados visual.
#
#  Secuencia de funcionamiento:
#
#      VERDE  → AMARILLO → ROJO → VERDE
#
# =====================================================================================


# -------------------------------------------------------------------------------------
# Importacion de librerias
# -------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import tkinter as tk


# -------------------------------------------------------------------------------------
# Definicion de pines
# -------------------------------------------------------------------------------------

pin_rojo = 17
pin_amarillo = 27
pin_verde = 22


# -------------------------------------------------------------------------------------
# Definicion de tiempos (milisegundos)
# -------------------------------------------------------------------------------------

tiempo_verde = 5000
tiempo_amarillo = 2000
tiempo_rojo = 5000


# -------------------------------------------------------------------------------------
# Configuracion inicial del sistema GPIO
# -------------------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_verde, GPIO.OUT)
GPIO.setup(pin_amarillo, GPIO.OUT)
GPIO.setup(pin_rojo, GPIO.OUT)


# -------------------------------------------------------------------------------------
# Variables del sistema
# -------------------------------------------------------------------------------------

estado_actual = "VERDE"


# -------------------------------------------------------------------------------------
# Funcion que actualiza el estado del semaforo
# -------------------------------------------------------------------------------------

def actualizar_semaforo():

    global estado_actual

    # =====================================================
    # ESTADO VERDE
    # =====================================================

    if estado_actual == "VERDE":

        print("Semaforo en VERDE")

        GPIO.output(pin_verde, GPIO.HIGH)
        GPIO.output(pin_amarillo, GPIO.LOW)
        GPIO.output(pin_rojo, GPIO.LOW)

        canvas.itemconfig(led_verde, fill="green")
        canvas.itemconfig(led_amarillo, fill="gray")
        canvas.itemconfig(led_rojo, fill="gray")

        estado_actual = "AMARILLO"

        ventana.after(tiempo_verde, actualizar_semaforo)


    # =====================================================
    # ESTADO AMARILLO
    # =====================================================

    elif estado_actual == "AMARILLO":

        print("Semaforo en AMARILLO")

        GPIO.output(pin_verde, GPIO.LOW)
        GPIO.output(pin_amarillo, GPIO.HIGH)
        GPIO.output(pin_rojo, GPIO.LOW)

        canvas.itemconfig(led_verde, fill="gray")
        canvas.itemconfig(led_amarillo, fill="yellow")
        canvas.itemconfig(led_rojo, fill="gray")

        estado_actual = "ROJO"

        ventana.after(tiempo_amarillo, actualizar_semaforo)


    # =====================================================
    # ESTADO ROJO
    # =====================================================

    elif estado_actual == "ROJO":

        print("Semaforo en ROJO")

        GPIO.output(pin_verde, GPIO.LOW)
        GPIO.output(pin_amarillo, GPIO.LOW)
        GPIO.output(pin_rojo, GPIO.HIGH)

        canvas.itemconfig(led_verde, fill="gray")
        canvas.itemconfig(led_amarillo, fill="gray")
        canvas.itemconfig(led_rojo, fill="red")

        estado_actual = "VERDE"

        ventana.after(tiempo_rojo, actualizar_semaforo)


# -------------------------------------------------------------------------------------
# Creacion de la interfaz grafica
# -------------------------------------------------------------------------------------

ventana = tk.Tk()
ventana.title("Sys On Chip - Semaforo")

canvas = tk.Canvas(ventana, width=200, height=350)
canvas.pack()

# LED rojo
led_rojo = canvas.create_oval(60, 40, 140, 120, fill="gray")

# LED amarillo
led_amarillo = canvas.create_oval(60, 140, 140, 220, fill="gray")

# LED verde
led_verde = canvas.create_oval(60, 240, 140, 320, fill="gray")


# -------------------------------------------------------------------------------------
# Inicio del sistema
# -------------------------------------------------------------------------------------

print("Sistema de semaforo iniciado")

ventana.after(1000, actualizar_semaforo)


# -------------------------------------------------------------------------------------
# Ejecucion de la interfaz grafica
# -------------------------------------------------------------------------------------

try:

    ventana.mainloop()

finally:

    GPIO.cleanup()

    print("GPIO liberado correctamente")
    print("Programa finalizado")
