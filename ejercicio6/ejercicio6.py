# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 6 – Semaforo con boton usando interrupciones
#
#  Descripcion general:
#  Este programa implementa un semaforo vehicular con solicitud peatonal
#  utilizando interrupciones GPIO en la Raspberry Pi.
#
#  A diferencia del ejercicio anterior, donde el boton era consultado
#  constantemente dentro del bucle principal (polling), aqui utilizamos
#  una interrupcion que se ejecuta automaticamente cuando el boton es
#  presionado.
#
#  Esto permite construir sistemas mas eficientes y reactivos.
#
#  La rutina de interrupcion sigue buenas practicas:
#
#   1) Es corta y eficiente
#   2) No contiene retardos
#   3) Solo genera un evento
#   4) Implementa debounce por software
#
#  Secuencia de funcionamiento:
#
#      VERDE ----(boton)----> AMARILLO → ROJO → VERDE
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

GPIO.setup(pin_boton, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# -------------------------------------------------------------------------------------
# Variables del sistema
# -------------------------------------------------------------------------------------

estado_actual = "VERDE"

solicitud_peaton = False

ultimo_evento = 0


# -------------------------------------------------------------------------------------
# Rutina de interrupcion del boton
# -------------------------------------------------------------------------------------

def ISR_boton(channel):

    global solicitud_peaton
    global ultimo_evento
    global estado_actual

    tiempo_actual = time.time()

    # Eliminacion de rebotes
    if tiempo_actual - ultimo_evento > tiempo_debounce:

        # Solo aceptar solicitud si el semaforo esta en VERDE
        if estado_actual == "VERDE":

            solicitud_peaton = True
            print("Interrupcion: solicitud de peaton")

        ultimo_evento = tiempo_actual


# -------------------------------------------------------------------------------------
# Asociacion de la interrupcion GPIO
# -------------------------------------------------------------------------------------

GPIO.add_event_detect(
    pin_boton,
    GPIO.FALLING,
    callback=ISR_boton
)


# -------------------------------------------------------------------------------------
# Bucle principal del programa
# -------------------------------------------------------------------------------------

print("Sistema de semaforo iniciado")


try:

    while True:

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

                if solicitud_peaton:

                    solicitud_peaton = False
                    estado_actual = "AMARILLO"
                    break

                time.sleep(0.01)

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
