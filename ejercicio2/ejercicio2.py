# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 2 – Semaforo vehicular con Raspberry Pi
#
#  Descripcion general:
#  Este programa implementa un semaforo vehicular simple utilizando
#  tres pines GPIO de la Raspberry Pi.
#
#  El objetivo del ejercicio es aprender a controlar multiples salidas
#  digitales y construir una secuencia de estados utilizando retardos
#  de tiempo.
#
#  En este ejercicio aprenderemos:
#
#   1) Como controlar multiples pines GPIO.
#   2) Como estructurar un sistema basado en estados simples.
#   3) Como utilizar retardos para generar secuencias de control.
#   4) Como organizar codigo de sistemas embebidos en Python.
#
#  Secuencia de funcionamiento:
#
#      VERDE  → AMARILLO → ROJO → VERDE
#
#  Tiempos de cada estado:
#
#      Verde     : 5 segundos
#      Amarillo  : 2 segundos
#      Rojo      : 5 segundos
#
# =====================================================================================


# -------------------------------------------------------------------------------------
# Importacion de librerias
# -------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import time


# -------------------------------------------------------------------------------------
# Definicion de pines
# -------------------------------------------------------------------------------------

pin_rojo = 17
pin_amarillo = 27
pin_verde = 22


# -------------------------------------------------------------------------------------
# Definicion de tiempos (segundos)
# -------------------------------------------------------------------------------------

tiempo_verde = 5
tiempo_amarillo = 2
tiempo_rojo = 5


# -------------------------------------------------------------------------------------
# Configuracion inicial del sistema GPIO
# -------------------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_verde, GPIO.OUT)
GPIO.setup(pin_amarillo, GPIO.OUT)
GPIO.setup(pin_rojo, GPIO.OUT)


# -------------------------------------------------------------------------------------
# Bucle principal del programa
# -------------------------------------------------------------------------------------

print("Sistema de semaforo iniciado")


try:

    while True:

        # =====================================================
        # ESTADO VERDE
        # =====================================================

        print("Semaforo en VERDE")

        GPIO.output(pin_verde, GPIO.HIGH)
        GPIO.output(pin_amarillo, GPIO.LOW)
        GPIO.output(pin_rojo, GPIO.LOW)

        time.sleep(tiempo_verde)


        # =====================================================
        # ESTADO AMARILLO
        # =====================================================

        print("Semaforo en AMARILLO")

        GPIO.output(pin_verde, GPIO.LOW)
        GPIO.output(pin_amarillo, GPIO.HIGH)
        GPIO.output(pin_rojo, GPIO.LOW)

        time.sleep(tiempo_amarillo)


        # =====================================================
        # ESTADO ROJO
        # =====================================================

        print("Semaforo en ROJO")

        GPIO.output(pin_verde, GPIO.LOW)
        GPIO.output(pin_amarillo, GPIO.LOW)
        GPIO.output(pin_rojo, GPIO.HIGH)

        time.sleep(tiempo_rojo)


# -------------------------------------------------------------------------------------
# Manejo de interrupcion por teclado
# -------------------------------------------------------------------------------------

except KeyboardInterrupt:

    print("\nInterrupcion detectada. Finalizando programa...")


# -------------------------------------------------------------------------------------
# Liberacion de recursos GPIO
# -------------------------------------------------------------------------------------

finally:

    GPIO.cleanup()

    print("GPIO liberado correctamente")
    print("Programa finalizado")
