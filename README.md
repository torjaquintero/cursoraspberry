# cursoraspberry

# Ejercicio No. 1

Este ejercicio introduce el control básico de hardware utilizando los pines GPIO de una **Raspberry Pi 5** mediante el lenguaje Python. El programa implementa el clásico ejemplo de **parpadeo de un LED**, configurando un pin GPIO como salida digital y alternando su estado lógico entre encendido y apagado con un intervalo de un segundo. A través de este ejemplo se presentan conceptos fundamentales de programación en sistemas embebidos, como la configuración del modo de numeración de pines, la escritura de niveles lógicos HIGH y LOW, el uso de retardos temporales y el manejo adecuado de interrupciones del usuario. Además, el código incorpora buenas prácticas de desarrollo al incluir manejo de excepciones y liberación de los recursos GPIO al finalizar el programa, proporcionando así una primera aproximación clara a la interacción entre software y hardware en plataformas embebidas basadas en Raspberry Pi.


# Ejercicio No. 2

Este ejercicio implementa un **sistema básico de semáforo vehicular utilizando la Raspberry Pi y la librería RPi.GPIO en Python**. El programa controla tres LEDs conectados a los pines GPIO que representan las señales **verde, amarillo y rojo**, generando una secuencia de estados típica de señalización de tráfico. El objetivo del ejercicio es introducir conceptos fundamentales del diseño de sistemas embebidos, como el **control de múltiples salidas digitales, la implementación de sistemas basados en estados y la gestión de temporización mediante retardos de software**. Este ejercicio forma parte de una serie de prácticas progresivas orientadas al aprendizaje de **programación de hardware con Raspberry Pi y desarrollo de sistemas electrónicos embebidos**.

# Ejercicio No. 3

Este ejercicio introduce la integración entre **control de hardware en Raspberry Pi y visualización mediante una interfaz gráfica en Python**. El programa controla un LED físico conectado al **GPIO17** utilizando la librería `RPi.GPIO`, mientras que una ventana gráfica desarrollada con **Tkinter** muestra un LED virtual cuyo color refleja el estado del dispositivo real. El sistema alterna automáticamente entre encendido y apagado cada segundo, actualizando tanto el hardware como la representación visual. El objetivo del ejercicio es familiarizarse con la creación de **interfaces gráficas simples, el uso del objeto Canvas para representar dispositivos electrónicos y la sincronización entre GPIO y aplicaciones gráficas mediante tareas periódicas con el método `after()`**. Este ejercicio forma parte de una serie progresiva orientada al aprendizaje práctico de **programación de sistemas embebidos con Raspberry Pi**.
