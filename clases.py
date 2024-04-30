# Importando librerias
import pygame
import sys
import math
import matplotlib.pyplot as plt
import numpy as np

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)  # Verde oscuro para la mesa de billar
BLUE = (0, 0, 255)

# Dimensiones de la ventana
WIDTH, HEIGHT = 1000, 600
GRAPH_WIDTH = 200
GRAPH_HEIGHT = 200

KINDS_OF_COLLISION = ['Inelastica', 'Elastica', 'Completamente inelastica']

# Tiempo entre cada vez que se dibuja el escenario
TIME = 0.001

# Clase que contiene el escenario 
class Scenenary: 
    # Constructor 
    def __init__(self, kind, *balls):
        assert(kind in KINDS_OF_COLLISION)
        self.kind = kind
        self.balls = balls
        self.kinetic_energy = []
        self.momentum = []
        self.momentum_x = []
        self.momentum_y = []
    # Actualizar información de momentum y energía cinética total 
    def updateData(self):
        k = 0
        for ball in self.balls: 
            k += ball.kinetic_energy()
        m = [0,0,0]
        for ball in self.balls: 
            m += ball.momentum()
        # Añadiendo valores a historial 
        self.kinetic_energy.append(k)
        self.momentum.append(m[0])
        self.momentum.append(m[1])
        self.momentum.append(m[2])
    # Método para chequear coliciones entre todas las bolas que se encuentran en el escenario
    def checkCollision():
        for ball in self.balls: 
            otherBalls = [x for x in self.balls if x != ball]
            for otherBall in otherBalls:
                ball.checkCollision(otherBall, self.kind)


# Clase para representar una bola
class Ball:
    # Constructor
    def __init__(self, x = 0, y = 0, radius = 1, mass = 1, speed = 1, angle = 0, color = "r"):
        """
        Constructor de clase ball recibe los siguientes argumentos: 
        x : coordenada inicial en x - 0 por default
        y : coordenada inicial en y - 0 por default
        radius: Radio de la bola (m) - 1 por default 
        speed: Velocidad de la bola (m/s) - 1 por default
        angulo respecto a la horizontal de la bola (º) - 0 por default
        color: Color con el que se verá la bola - rojo por default
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        # Transformando ángulo obtenido a radianes (con estos funciona la libreria math de python)
        self.angle = math.radians(angle % 360)
        # Descomponiendo velocidad en ejes
        self.vy = math.sin(self.angle) * self.speed 
        self.vx = math.cos(self.angle) * self.speed

    # Función que retorna energía cinetica actual de la bola
    def kinetic_energy(self):
        return .5 * self.mass * self.speed**2

    # Retorna tripla con momentum total y momentum en cada eje
    def momentum(self):
        momentum = self.mass * self.speed
        momentum_x = self.mass * self.vx
        momentum_y = self.mass * self.vy
        return (momentum, momentum_x, momentum_y)
    
    # Método que actualiza la ubicación actual de la bola
    def update(self):
        self.x = self.vx * TIME
        self.y = self.vy * TIME

    # Helper que dibuja la bola en pantalla
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    # Chequeamos posible collision: 
    def checkCollision(self, other : ball, kind):       
        #Chequeando si están en contacto
        distance = sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        # Sí no están en contacto ya sabemos que no hay collision 
        if distance > self.radius + other.radius:
            return False
        elif kind == KINDS_OF_COLLISION[2]:
            pass 
        elif kind == KINDS_OF_COLLISION[1] or KINDS_OF_COLLISION == KINDS_OF_COLLISION[0]:
            pass 
        # En caso de que no sea alguna de las 3 colisiones tiramos error
        raise Exception(f"La colision {kind} no es una de las posibles colisiones {KINDS_OF_COLLISION}")


    # Método que chequea si la bola va a colicionar con una pared (no genera perdidas de energía cinetica)
    def check_boundary_collision(self):
        if self.x - self.radius <= 50 or self.x + self.radius >= WIDTH - 50:
            self.angle = math.pi - self.angle
        if self.y - self.radius <= 50 or self.y + self.radius >= HEIGHT - 50:
            self.angle = 2 * math.pi - self.angle