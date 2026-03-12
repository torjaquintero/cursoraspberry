# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 1 – Parpadeo de un LED con Raspberry Pi
#
#  Descripción general:
#  Este programa implementa el ejemplo clásico de control de un LED
#  utilizando los pines GPIO de la Raspberry Pi.
#
#  El objetivo del ejercicio es introducir los conceptos básicos de
#  interacción entre software y hardware en sistemas embebidos.
#
#  En este ejercicio aprenderemos:
#
#   1) Cómo configurar el modo de numeración de los pines GPIO.
#   2) Cómo declarar un pin como salida digital.
#   3) Cómo escribir niveles lógicos HIGH y LOW.
#   4) Cómo generar retardos utilizando la librería time.
#   5) Cómo liberar correctamente los recursos del sistema.
#
#  Funcionamiento del programa:
#
#      LED ENCENDIDO  → espera 1 segundo
#      LED APAGADO    → espera 1 segundo
#
#  Este proceso se repite continuamente hasta que el usuario
#  interrumpe el programa con CTRL + C.
#
# =====================================================================================


# -------------------------------------------------------------------------------------
# Importación de librerías
# -------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import time


# -------------------------------------------------------------------------------------
# Definición de pines
# -------------------------------------------------------------------------------------
# Usaremos la numeración BCM del procesador Broadcom.

pin_led = 17


# -------------------------------------------------------------------------------------
# Configuración inicial del sistema GPIO
# -------------------------------------------------------------------------------------

# Seleccionamos el modo de numeración BCM
GPIO.setmode(GPIO.BCM)

# Configuramos el pin del LED como salida digital
GPIO.setup(pin_led, GPIO.OUT)


# -------------------------------------------------------------------------------------
# Bucle principal del programa
# -------------------------------------------------------------------------------------
# En Raspberry Pi no existe una función loop() como en Arduino,
# por lo que utilizamos un bucle infinito while True.

print("Sistema iniciado")
print("Controlando LED en GPIO", pin_led)

try:

    while True:

        # -----------------------------------------------------
        # Encender el LED
        # -----------------------------------------------------
        print("Encendiendo LED")

        GPIO.output(pin_led, GPIO.HIGH)

        # Espera de 1 segundo
        time.sleep(1)


        # -----------------------------------------------------
        # Apagar el LED
        # -----------------------------------------------------
        print("Apagando LED")

        GPIO.output(pin_led, GPIO.LOW)

        # Espera de 1 segundo
        time.sleep(1)


# -------------------------------------------------------------------------------------
# Manejo de interrupción por teclado
# -------------------------------------------------------------------------------------
# Se ejecuta cuando el usuario presiona CTRL + C.

except KeyboardInterrupt:

    print("\nInterrupción detectada. Finalizando programa...")


# -------------------------------------------------------------------------------------
# Liberación de recursos GPIO
# -------------------------------------------------------------------------------------
# Es una buena práctica limpiar los pines antes de terminar
# la ejecución del programa.

finally:

    GPIO.cleanup()

    print("GPIO liberado correctamente")
    print("Programa finalizado")
