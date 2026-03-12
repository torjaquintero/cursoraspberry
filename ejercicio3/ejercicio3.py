# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 3 – Control de LED con interfaz grafica (Tkinter)
#
#  Descripcion general:
#  Este programa extiende el Ejercicio No.1 agregando una interfaz grafica
#  que permite visualizar el estado del LED conectado a la Raspberry Pi.
#
#  El sistema controla un LED fisico conectado al GPIO17 y al mismo tiempo
#  muestra un LED virtual en una ventana grafica utilizando la libreria Tkinter.
#
#  El LED virtual cambia de color dependiendo del estado del LED real.
#
#  En este ejercicio aprenderemos:
#
#   1) Como crear una interfaz grafica simple con Tkinter.
#   2) Como representar un LED virtual utilizando un objeto Canvas.
#   3) Como sincronizar hardware GPIO con una interfaz grafica.
#   4) Como programar tareas periodicas con el metodo after().
#
#  Funcionamiento del sistema:
#
#      LED ENCENDIDO  → circulo rojo
#      LED APAGADO    → circulo gris
#
#  El sistema cambia automaticamente entre ambos estados cada segundo.
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

pin_led = 17


# -------------------------------------------------------------------------------------
# Configuracion inicial del sistema GPIO
# -------------------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led, GPIO.OUT)


# -------------------------------------------------------------------------------------
# Variables del sistema
# -------------------------------------------------------------------------------------

estado_led = False


# -------------------------------------------------------------------------------------
# Funcion que alterna el estado del LED
# -------------------------------------------------------------------------------------

def actualizar_led():

    global estado_led

    # Cambiar estado
    estado_led = not estado_led

    if estado_led:

        GPIO.output(pin_led, GPIO.HIGH)
        canvas.itemconfig(led_virtual, fill="red")

    else:

        GPIO.output(pin_led, GPIO.LOW)
        canvas.itemconfig(led_virtual, fill="gray")

    # Ejecutar nuevamente la funcion despues de 1 segundo
    ventana.after(1000, actualizar_led)


# -------------------------------------------------------------------------------------
# Creacion de la interfaz grafica
# -------------------------------------------------------------------------------------

ventana = tk.Tk()
ventana.title("Sys On Chip - Monitor de LED")

canvas = tk.Canvas(ventana, width=200, height=200)
canvas.pack()

# Creacion del LED virtual (circulo)
led_virtual = canvas.create_oval(50, 50, 150, 150, fill="gray")


# -------------------------------------------------------------------------------------
# Inicio del sistema
# -------------------------------------------------------------------------------------

print("Sistema iniciado")

ventana.after(1000, actualizar_led)


# -------------------------------------------------------------------------------------
# Ejecucion de la interfaz grafica
# -------------------------------------------------------------------------------------

try:

    ventana.mainloop()

finally:

    GPIO.cleanup()

    print("GPIO liberado correctamente")
    print("Programa finalizado")
