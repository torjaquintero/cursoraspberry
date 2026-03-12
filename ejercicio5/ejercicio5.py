# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 5 – Semaforo con boton de peaton
#
#  Descripcion general:
#  Este programa implementa un semaforo vehicular controlado por la
#  Raspberry Pi con la posibilidad de generar una solicitud peatonal
#  mediante un pulsador.
#
#  Cuando el sistema se encuentra en estado VERDE, el peaton puede
#  presionar el boton para solicitar el cambio del semaforo.
#
#  Si el boton se presiona durante los estados AMARILLO o ROJO,
#  la solicitud sera ignorada.
#
#  El programa incluye proteccion contra rebote (debounce) por software
#  para evitar multiples activaciones del boton.
#
#  Secuencia de funcionamiento:
#
#      VERDE ----(boton)----> AMARILLO → ROJO → VERDE
#
#  En este ejercicio aprenderemos:
#
#   1) Como leer entradas digitales en Raspberry Pi
#   2) Como implementar logica dependiente del estado del sistema
#   3) Como implementar debounce por software
#   4) Como construir una maquina de estados simple
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

pin_boton = 23


# -------------------------------------------------------------------------------------
# Definicion de tiempos (segundos)
# -------------------------------------------------------------------------------------

tiempo_verde = 5
tiempo_amarillo = 2
tiempo_rojo = 5

tiempo_debounce = 0.2


# -------------------------------------------------------------------------------------
# Configuracion inicial del sistema GPIO
# -------------------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_verde, GPIO.OUT)
GPIO.setup(pin_amarillo, GPIO.OUT)
GPIO.setup(pin_rojo, GPIO.OUT)

# El boton usa resistencia interna pull-up
GPIO.setup(pin_boton, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# -------------------------------------------------------------------------------------
# Variables del sistema
# -------------------------------------------------------------------------------------

estado_actual = "VERDE"

solicitud_peaton = False

ultimo_boton = 0


# -------------------------------------------------------------------------------------
# Bucle principal del programa
# -------------------------------------------------------------------------------------

print("Sistema de semaforo iniciado")


try:

    while True:

        tiempo_actual = time.time()

        # -------------------------------------------------
        # Lectura del boton con eliminacion de rebotes
        # -------------------------------------------------

        if GPIO.input(pin_boton) == GPIO.LOW:

            if tiempo_actual - ultimo_boton > tiempo_debounce:

                ultimo_boton = tiempo_actual

                if estado_actual == "VERDE":

                    print("Solicitud de peaton detectada")
                    solicitud_peaton = True


        # =====================================================
        # ESTADO VERDE
        # =====================================================

        if estado_actual == "VERDE":

            print("Semaforo en VERDE")

            GPIO.output(pin_verde, GPIO.HIGH)
            GPIO.output(pin_amarillo, GPIO.LOW)
            GPIO.output(pin_rojo, GPIO.LOW)

            inicio = time.time()

            while time.time() - inicio < tiempo_verde:

                # Durante el verde seguimos verificando el boton
                tiempo_actual = time.time()

                if GPIO.input(pin_boton) == GPIO.LOW:

                    if tiempo_actual - ultimo_boton > tiempo_debounce:

                        ultimo_boton = tiempo_actual
                        solicitud_peaton = True
                        print("Peaton solicita cruce")

                if solicitud_peaton:
                    break

                time.sleep(0.01)

            if solicitud_peaton:
                solicitud_peaton = False
                estado_actual = "AMARILLO"

            else:
                estado_actual = "AMARILLO"


        # =====================================================
        # ESTADO AMARILLO
        # =====================================================

        elif estado_actual == "AMARILLO":

            print("Semaforo en AMARILLO")

            GPIO.output(pin_verde, GPIO.LOW)
            GPIO.output(pin_amarillo, GPIO.HIGH)
            GPIO.output(pin_rojo, GPIO.LOW)

            time.sleep(tiempo_amarillo)

            estado_actual = "ROJO"


        # =====================================================
        # ESTADO ROJO
        # =====================================================

        elif estado_actual == "ROJO":

            print("Semaforo en ROJO")

            GPIO.output(pin_verde, GPIO.LOW)
            GPIO.output(pin_amarillo, GPIO.LOW)
            GPIO.output(pin_rojo, GPIO.HIGH)

            time.sleep(tiempo_rojo)

            estado_actual = "VERDE"


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
