import turtle
import time
import random
import os

# ==========================================
# UNIDAD 4: PERSISTENCIA DE DATOS & FUNCIONAL
# ==========================================

def obtener_max_puntaje():
    """Función para leer el récord desde un archivo."""
    if not os.path.exists("record.txt"):
        with open("record.txt", "w") as f:
            f.write("0")
        return 0
    with open("record.txt", "r") as f:
        return int(f.read())

def guardar_max_puntaje(nuevo_record):
    """Función para escribir el récord en el archivo."""
    with open("record.txt", "w") as f:
        f.write(str(nuevo_record))

# Ejemplo de Programación Funcional: Lambdas para validaciones puras
esta_fuera_limites = lambda pos, limite: abs(pos) > limite
calcular_distancia = lambda pos1, pos2: pos1.distance(pos2)

# ==========================================
# UNIDAD 1 & 2: CONFIGURACIÓN Y ARQUITECTURA
# ==========================================

retraso = 0.1
marcador = 0
max_puntaje = obtener_max_puntaje()

ventana = turtle.Screen()
ventana.title("Snake Game - Proyecto Integrador")
ventana.bgcolor("black")
ventana.setup(width=600, height=600)
ventana.tracer(0)

# Cabeza
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("white")
cabeza.penup()
cabeza.goto(0,0)
cabeza.direction = "stop"

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0,100)

# ==========================================
# UNIDAD 3: ESTRUCTURAS DE DATOS (LISTAS)
# ==========================================
segmentos = [] # Lista para el cuerpo de la serpiente

# Texto del marcador
texto = turtle.Turtle()
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0, 260)
texto.write(f"Puntos: 0  Récord: {max_puntaje}", align="center", font=("Courier", 24, "normal"))

# Funciones de control
def arriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"
def abajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"
def izquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"
def derecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"

def mover():
    if cabeza.direction == "up":
        cabeza.sety(cabeza.ycor() + 20)
    if cabeza.direction == "down":
        cabeza.sety(cabeza.ycor() - 20)
    if cabeza.direction == "left":
        cabeza.setx(cabeza.xcor() - 20)
    if cabeza.direction == "right":
        cabeza.setx(cabeza.xcor() + 20)

# Teclado
ventana.listen()
ventana.onkeypress(arriba, "w")
ventana.onkeypress(abajo, "s")
ventana.onkeypress(izquierda, "a")
ventana.onkeypress(derecha, "d")

# ==========================================
# UNIDAD 3 & 4: BUCLE PRINCIPAL E INTEGRACIÓN
# ==========================================

while True:
    ventana.update()

    # Colisión con bordes (Usando la lógica de la Unidad 4)
    if esta_fuera_limites(cabeza.xcor(), 280) or esta_fuera_limites(cabeza.ycor(), 280):
        time.sleep(1)
        cabeza.goto(0,0)
        cabeza.direction = "stop"
        
        # Esconder segmentos (Reiniciar juego)
        for s in segmentos:
            s.goto(1000, 1000)
        segmentos.clear()
        
        marcador = 0
        texto.clear()
        texto.write(f"Puntos: {marcador}  Récord: {max_puntaje}", align="center", font=("Courier", 24, "normal"))

    # Colisión con comida
    if calcular_distancia(cabeza, comida) < 20:
        comida.goto(random.randint(-280, 280), random.randint(-280, 280))
        
        # Nuevo segmento (Estructura de datos - Unidad 3)
        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")
        nuevo_segmento.color("grey")
        nuevo_segmento.penup()
        segmentos.append(nuevo_segmento)

        marcador += 1
        if marcador > max_puntaje:
            max_puntaje = marcador
            guardar_max_puntaje(max_puntaje) # Persistencia - Unidad 4
            
        texto.clear()
        texto.write(f"Puntos: {marcador}  Récord: {max_puntaje}", align="center", font=("Courier", 24, "normal"))

    # Mover el cuerpo (Lógica de seguimiento)
    for i in range(len(segmentos) - 1, 0, -1):
        x = segmentos[i-1].xcor()
        y = segmentos[i-1].ycor()
        segmentos[i].goto(x, y)

    if len(segmentos) > 0:
        segmentos[0].goto(cabeza.xcor(), cabeza.ycor())

    mover()

    # Colisión con el propio cuerpo
    for s in segmentos:
        if s.distance(cabeza) < 20:
            time.sleep(1)
            cabeza.goto(0,0)
            cabeza.direction = "stop"
            for seg in segmentos:
                seg.goto(1000, 1000)
            segmentos.clear()
            marcador = 0
            texto.clear()
            texto.write(f"Puntos: {marcador}  Récord: {max_puntaje}", align="center", font=("Courier", 24, "normal"))

    time.sleep(retraso)