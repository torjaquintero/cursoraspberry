# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 8 – Semaforo con modos de funcionamiento
#
#  Descripcion general:
#  Este programa extiende el sistema de semaforo del ejercicio anterior
#  agregando modos de operacion seleccionables desde la interfaz grafica.
#
#  Modos disponibles:
#
#   Modo NORMAL
#       Funcionamiento clasico del semaforo
#
#           VERDE → AMARILLO → ROJO → VERDE
#
#   Modo INTERMITENTE
#       El semaforo entra en modo precaucion
#
#           AMARILLO ON ↔ AMARILLO OFF
#
#  Caracteristicas del sistema:
#
#   - Control GPIO de LEDs
#   - Interrupcion por boton de peaton
#   - Eliminacion de rebotes
#   - Maquina de estados
#   - Interfaz grafica con Tkinter
#   - Seleccion de modo de operacion
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
# Definicion de tiempos
# -------------------------------------------------------------------------------------

tiempo_verde = 5
tiempo_amarillo = 2
tiempo_rojo = 5

tiempo_intermitente = 0.5

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

modo = "NORMAL"

solicitud_peaton = False

ultimo_evento = 0

inicio_estado = time.time()

estado_intermitente = False


# -------------------------------------------------------------------------------------
# Rutina de interrupcion del boton
# -------------------------------------------------------------------------------------

def ISR_boton(channel):

    global solicitud_peaton
    global ultimo_evento
    global estado_actual
    global modo

    tiempo_actual = time.time()

    if tiempo_actual - ultimo_evento > tiempo_debounce:

        if estado_actual == "VERDE" and modo == "NORMAL":

            solicitud_peaton = True

            mensaje.set("Peaton detectado")

            canvas.itemconfig(indicador_boton, fill="blue")

            print("Solicitud peaton detectada")

        ultimo_evento = tiempo_actual


GPIO.add_event_detect(pin_boton, GPIO.FALLING, callback=ISR_boton)


# -------------------------------------------------------------------------------------
# Funciones de cambio de modo
# -------------------------------------------------------------------------------------

def modo_normal():

    global modo
    global estado_actual
    global inicio_estado

    modo = "NORMAL"

    estado_actual = "VERDE"

    inicio_estado = time.time()

    mensaje.set("Modo NORMAL")

    print("Modo NORMAL activado")


def modo_intermitente():

    global modo

    modo = "INTERMITENTE"

    mensaje.set("Modo INTERMITENTE")

    print("Modo INTERMITENTE activado")


# -------------------------------------------------------------------------------------
# Maquina de estados del sistema
# -------------------------------------------------------------------------------------

def actualizar_sistema():

    global estado_actual
    global solicitud_peaton
    global inicio_estado
    global estado_intermitente
    global modo

    tiempo_actual = time.time()

    # =====================================================
    # MODO NORMAL
    # =====================================================

    if modo == "NORMAL":

        # -------------------------
        # ESTADO VERDE
        # -------------------------

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

            elif tiempo_actual - inicio_estado >= tiempo_verde:

                estado_actual = "AMARILLO"
                inicio_estado = tiempo_actual


        # -------------------------
        # ESTADO AMARILLO
        # -------------------------

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


        # -------------------------
        # ESTADO ROJO
        # -------------------------

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


    # =====================================================
    # MODO INTERMITENTE
    # =====================================================

    elif modo == "INTERMITENTE":

        if tiempo_actual - inicio_estado >= tiempo_intermitente:

            inicio_estado = tiempo_actual

            estado_intermitente = not estado_intermitente

            if estado_intermitente:

                GPIO.output(pin_verde, GPIO.LOW)
                GPIO.output(pin_amarillo, GPIO.HIGH)
                GPIO.output(pin_rojo, GPIO.LOW)

                canvas.itemconfig(led_verde, fill="gray")
                canvas.itemconfig(led_amarillo, fill="yellow")
                canvas.itemconfig(led_rojo, fill="gray")

            else:

                GPIO.output(pin_amarillo, GPIO.LOW)

                canvas.itemconfig(led_amarillo, fill="gray")


    ventana.after(50, actualizar_sistema)


# -------------------------------------------------------------------------------------
# Creacion de interfaz grafica
# -------------------------------------------------------------------------------------

ventana = tk.Tk()

ventana.title("Sys On Chip - Semaforo Inteligente")

canvas = tk.Canvas(ventana, width=240, height=420)

canvas.pack()


# LEDs del semaforo

led_rojo = canvas.create_oval(80, 40, 160, 120, fill="gray")

led_amarillo = canvas.create_oval(80, 150, 160, 230, fill="gray")

led_verde = canvas.create_oval(80, 260, 160, 340, fill="gray")


# Indicador boton

canvas.create_text(120, 360, text="Boton")

indicador_boton = canvas.create_oval(105, 370, 135, 400, fill="gray")


# Mensaje

mensaje = tk.StringVar()

mensaje.set("Sistema iniciado")

label_mensaje = tk.Label(ventana, textvariable=mensaje)

label_mensaje.pack()


# -------------------------------------------------------------------------------------
# Botones de modo
# -------------------------------------------------------------------------------------

frame_botones = tk.Frame(ventana)

frame_botones.pack(pady=10)

boton_normal = tk.Button(
    frame_botones,
    text="Modo Normal",
    command=modo_normal,
    width=15
)

boton_normal.grid(row=0, column=0, padx=10)


boton_intermitente = tk.Button(
    frame_botones,
    text="Modo Intermitente",
    command=modo_intermitente,
    width=15
)

boton_intermitente.grid(row=0, column=1, padx=10)


# -------------------------------------------------------------------------------------
# Inicio del sistema
# -------------------------------------------------------------------------------------

print("Sistema iniciado")

inicio_estado = time.time()

ventana.after(50, actualizar_sistema)


# -------------------------------------------------------------------------------------
# Ejecucion del programa
# -------------------------------------------------------------------------------------

try:

    ventana.mainloop()

finally:

    GPIO.cleanup()

    print("GPIO liberado correctamente")
