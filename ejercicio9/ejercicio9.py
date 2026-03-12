# =====================================================================================
#  Bienvenidos a Sys On Chip
# =====================================================================================
#  Ejercicio No. 9 – Semaforo con display de cuenta regresiva
#
#  Descripcion general:
#  Este ejercicio extiende el Ejercicio 8 agregando un display digital
#  que muestra el tiempo restante de cada estado del semaforo.
#
#  El display se encuentra a la derecha del semaforo y cambia de color
#  segun el estado actual.
#
#  Caracteristicas:
#
#   - Control GPIO de LEDs
#   - Interrupcion por boton peatonal
#   - Eliminacion de rebotes
#   - Maquina de estados
#   - Interfaz grafica con Tkinter
#   - Modos de funcionamiento
#   - Display de cuenta regresiva
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
# Funcion para apagar LEDs
# -------------------------------------------------------------------------------------

def reset_salidas():

    GPIO.output(pin_verde, GPIO.LOW)
    GPIO.output(pin_amarillo, GPIO.LOW)
    GPIO.output(pin_rojo, GPIO.LOW)

    canvas.itemconfig(led_verde, fill="gray")
    canvas.itemconfig(led_amarillo, fill="gray")
    canvas.itemconfig(led_rojo, fill="gray")


# -------------------------------------------------------------------------------------
# Interrupcion del boton
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
# Cambio de modos
# -------------------------------------------------------------------------------------

def modo_normal():

    global modo
    global estado_actual
    global inicio_estado

    modo = "NORMAL"
    estado_actual = "VERDE"

    inicio_estado = time.time()

    reset_salidas()

    mensaje.set("Modo NORMAL")

    print("Modo NORMAL activado")


def modo_intermitente():

    global modo
    global inicio_estado
    global estado_intermitente

    modo = "INTERMITENTE"

    inicio_estado = time.time()
    estado_intermitente = False

    reset_salidas()

    mensaje.set("Modo INTERMITENTE")

    print("Modo INTERMITENTE activado")


# -------------------------------------------------------------------------------------
# Maquina de estados
# -------------------------------------------------------------------------------------

def actualizar_sistema():

    global estado_actual
    global solicitud_peaton
    global inicio_estado
    global estado_intermitente
    global modo

    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - inicio_estado


    # =====================================================
    # MODO NORMAL
    # =====================================================

    if modo == "NORMAL":

        # -------------------------
        # VERDE
        # -------------------------

        if estado_actual == "VERDE":

            GPIO.output(pin_verde, GPIO.HIGH)
            GPIO.output(pin_amarillo, GPIO.LOW)
            GPIO.output(pin_rojo, GPIO.LOW)

            canvas.itemconfig(led_verde, fill="green")
            canvas.itemconfig(led_amarillo, fill="gray")
            canvas.itemconfig(led_rojo, fill="gray")

            restante = int(tiempo_verde - tiempo_transcurrido)

            canvas.itemconfig(display, text=str(restante), fill="green")

            if solicitud_peaton:

                solicitud_peaton = False
                estado_actual = "AMARILLO"
                inicio_estado = tiempo_actual

            elif tiempo_transcurrido >= tiempo_verde:

                estado_actual = "AMARILLO"
                inicio_estado = tiempo_actual


        # -------------------------
        # AMARILLO
        # -------------------------

        elif estado_actual == "AMARILLO":

            GPIO.output(pin_verde, GPIO.LOW)
            GPIO.output(pin_amarillo, GPIO.HIGH)
            GPIO.output(pin_rojo, GPIO.LOW)

            canvas.itemconfig(led_verde, fill="gray")
            canvas.itemconfig(led_amarillo, fill="yellow")
            canvas.itemconfig(led_rojo, fill="gray")

            restante = int(tiempo_amarillo - tiempo_transcurrido)

            canvas.itemconfig(display, text=str(restante), fill="orange")

            if tiempo_transcurrido >= tiempo_amarillo:

                estado_actual = "ROJO"
                inicio_estado = tiempo_actual


        # -------------------------
        # ROJO
        # -------------------------

        elif estado_actual == "ROJO":

            GPIO.output(pin_verde, GPIO.LOW)
            GPIO.output(pin_amarillo, GPIO.LOW)
            GPIO.output(pin_rojo, GPIO.HIGH)

            canvas.itemconfig(led_verde, fill="gray")
            canvas.itemconfig(led_amarillo, fill="gray")
            canvas.itemconfig(led_rojo, fill="red")

            restante = int(tiempo_rojo - tiempo_transcurrido)

            canvas.itemconfig(display, text=str(restante), fill="red")

            if tiempo_transcurrido >= tiempo_rojo:

                estado_actual = "VERDE"
                inicio_estado = tiempo_actual

                canvas.itemconfig(indicador_boton, fill="gray")
                mensaje.set("Sistema en funcionamiento")


    # =====================================================
    # MODO INTERMITENTE
    # =====================================================

    elif modo == "INTERMITENTE":

        canvas.itemconfig(display, text="-", fill="yellow")

        if tiempo_actual - inicio_estado >= tiempo_intermitente:

            inicio_estado = tiempo_actual

            estado_intermitente = not estado_intermitente

            if estado_intermitente:

                GPIO.output(pin_amarillo, GPIO.HIGH)

                canvas.itemconfig(led_amarillo, fill="yellow")

            else:

                GPIO.output(pin_amarillo, GPIO.LOW)

                canvas.itemconfig(led_amarillo, fill="gray")


    ventana.after(50, actualizar_sistema)


# -------------------------------------------------------------------------------------
# Interfaz grafica (MISMA DEL EJERCICIO 8)
# -------------------------------------------------------------------------------------

ventana = tk.Tk()

ventana.title("Sys On Chip - Semaforo Inteligente")

canvas = tk.Canvas(ventana, width=240, height=420)

canvas.pack()


# LEDs

led_rojo = canvas.create_oval(80, 40, 160, 120, fill="gray")

led_amarillo = canvas.create_oval(80, 150, 160, 230, fill="gray")

led_verde = canvas.create_oval(80, 260, 160, 340, fill="gray")


# Display dentro del canvas

display = canvas.create_text(
    200,
    200,
    text="0",
    font=("Courier", 32, "bold"),
    fill="white"
)


# Indicador boton

canvas.create_text(120, 360, text="Boton")

indicador_boton = canvas.create_oval(105, 370, 135, 400, fill="gray")


# Mensaje

mensaje = tk.StringVar()

mensaje.set("Sistema iniciado")

label_mensaje = tk.Label(ventana, textvariable=mensaje)

label_mensaje.pack()


# -------------------------------------------------------------------------------------
# Botones
# -------------------------------------------------------------------------------------

frame_botones = tk.Frame(ventana)

frame_botones.pack(pady=10)

boton_normal = tk.Button(frame_botones, text="Modo Normal", command=modo_normal, width=15)

boton_normal.grid(row=0, column=0, padx=10)

boton_intermitente = tk.Button(frame_botones, text="Modo Intermitente", command=modo_intermitente, width=15)

boton_intermitente.grid(row=0, column=1, padx=10)


# -------------------------------------------------------------------------------------
# Inicio
# -------------------------------------------------------------------------------------

print("Sistema iniciado")

inicio_estado = time.time()

ventana.after(50, actualizar_sistema)


# -------------------------------------------------------------------------------------
# Ejecucion
# -------------------------------------------------------------------------------------

try:

    ventana.mainloop()

finally:

    GPIO.cleanup()

    print("GPIO liberado correctamente")
