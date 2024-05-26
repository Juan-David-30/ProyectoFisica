# Importando librerias
import pygame
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

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

velocity_factor = 0.1

# Clase que contiene el escenario 
class Scenenary: 
    # Constructor 
    def __init__(self, screen, *balls, e = 1):
        """
            Constructor de escenario, recibe como primer argumento posicional el tipo de colision
            El resto de argumentos posicionales son las bolas que formarán parte del escenario
            y como kwargument tenemos el coeficiente de restitución por default es 1 que es una colision completamente elastica
        """
        self.e = e
        self.balls = balls
        self.kinetic_energy = []
        self.momentum = []
        self.momentum_x = []
        self.momentum_y = []
        self.screen = screen
    # Actualizar información de momentum y energía cinética total 
    def updateData(self):
        k = 0
        for ball in self.balls: 
            ball.update()
            k += ball.calculate_kinetic_energy()
        mx = 0
        my = 0
        for ball in self.balls: 
            mx += ball.momentum()[1] 
            my += ball.momentum()[2]
            print(ball.momentum())
        # Añadiendo valores a historial 
        self.kinetic_energy.append(k)
        self.momentum_x.append(my)
        self.momentum_y.append(mx)
    # Método para chequear coliciones entre todas las bolas que se encuentran en el escenario
    def checkCollisions(self):
        # Chequeando por cada bola
        for ball1, ball2 in combinations(self.balls, 2):
            ball1.checkCollision(ball2, self.e)

    def handleEvent(self, event):
        for ball in self.balls:
            ball.handle_events(event)

    # Dibujando las bolas
    def draw(self):
        for ball in self.balls:
            ball.draw(self.screen)

# Clase para representar una bola
class Ball:
    # Constructor
    def __init__(self, x = 200, y = 200, radius = 30, mass = 1, speed = 10, angle = 0, color = RED):
        """
            Constructor de clase ball recibe los siguientes argumentos: 
            x : coordenada inicial en x - 200 por default
            y : coordenada inicial en y - 200 por default
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
        self.mass = mass
        # Transformando ángulo obtenido a radianes (con estos funciona la libreria math de python)
        self.angle = math.radians(angle % 360)
        # Descomponiendo velocidad en ejes
        self.vy = math.sin(self.angle) * self.speed 
        self.vx = math.cos(self.angle) * self.speed

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.dragging = False
        self.dragging_arrow = False
        self.arrow_end_x = self.x
        self.arrow_end_y = self.y

        self.updateArrowPos()

    def handle_events(self, event):
        global simulation_started

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.x - mouse_x
                    self.offset_y = self.y - mouse_y
            elif event.button == 3:  # Right click
                # Check if mouse is on the arrow tip of ball1
                if math.hypot(event.pos[0] - self.arrow_end_x, event.pos[1] - self.arrow_end_y) < 10:
                    self.dragging_arrow = True
                    self.arrow_offset_x = self.arrow_end_x - event.pos[0]
                    self.arrow_offset_y = self.arrow_end_y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging:
                    self.dragging = False
            elif event.button == 3:  # Right click
                if self.dragging_arrow:
                    self.dragging_arrow = False
                    # Calculate velocity based on arrow length and direction
                    dx = self.arrow_end_x - self.x
                    dy = self.arrow_end_y - self.y
                    velocity_factor = 0.0005 * math.sqrt(dx ** 2 + dy ** 2)
                    self.vx = dx * velocity_factor
                    self.vy = dy * velocity_factor
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.x = mouse_x + self.offset_x
                self.y = mouse_y + self.offset_y
                self.arrow_end_x = self.x
                self.arrow_end_y = self.y
                self.update_rect()
            elif self.dragging_arrow:
                self.arrow_end_x, self.arrow_end_y = event.pos[0] + self.arrow_offset_x, event.pos[1] + self.arrow_offset_y
        
        return True

    def updateArrowPos(self):
        dx = self.vx/velocity_factor 
        dy = self.vy / velocity_factor        
        self.arrow_end_x = self.x + dx
        self.arrow_end_y = self.y + dy

    def update_rect(self):
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    # Función que retorna energía cinetica actual de la bola
    def calculate_kinetic_energy(self):
        return .5 * self.mass * self.speed**2

    # Retorna tripla con momentum total y momentum en cada eje
    def momentum(self):
        momentum = self.mass * self.speed
        momentum_x = self.mass * self.vx
        momentum_y = self.mass * self.vy
        return (momentum, momentum_x, momentum_y)

    # Actualizar valores de velocidad 
    def updateSpeed(self, vx, vy):
        self.vx = vx 
        self.vy = vy
        self.speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
    
    # Método que actualiza la ubicación actual de la bola
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.arrow_end_x += self.vx
        self.arrow_end_y += self.vy

    # Helper que dibuja la bola en pantalla
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.arrow_end_x, self.arrow_end_y), 3)
        pygame.draw.circle(screen, WHITE, (int(self.arrow_end_x), int(self.arrow_end_y)), 5)

    # Chequeamos posible collisi
    # on: 
    def checkCollision(self, other, e):      
        #Chequeando si están en contacto
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        # Sí no están en contacto ya sabemos que no hay collision 
        if distance > self.radius + other.radius:
            return False
        else:
            # Para colisión inelastica y elastica podemos usar las mismas formulas basadas en el coeficiente de restitución
            vfx = (self.mass * self.vx + other.mass * (other.vx + e * (other.vx - self.vx))) / (self.mass + other.mass) 
            othervfx = (self.mass * (self.vx - vfx) + other.mass * other.vx) / other.mass
            vfy = (self.mass * self.vy + other.mass * (other.vy + e * (other.vy - self.vy))) / (self.mass + other.mass)
            othervfy = (self.mass * (self.vy - vfy) + other.mass * other.vy) / other.mass
            # Actualizando velocidades
            self.updateSpeed(vfx, vfy)
            other.updateSpeed(othervfx, othervfy)
            self.updateArrowPos()
            other.updateArrowPos()
            return True


    # Método que chequea si la bola va a colicionar con una pared (no genera perdidas de energía cinetica)
    def check_boundary_collision(self):
        if self.x - self.radius <= 50 or self.x + self.radius >= WIDTH - 50:
            self.angle = math.pi - self.angle
        if self.y - self.radius <= 50 or self.y + self.radius >= HEIGHT - 50:
            self.angle = 2 * math.pi - self.angle

coefficient = 1

while True:
    try:
        coefficient = float(input("Ingrese un coeficiente de restitución (entre 0 y 1): "))
        if 0 <= coefficient <= 1:
            break
    except ValueError:
        pass
    print("Valor no valido")

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Creación de las bolas (valores iniciales)
ball1 = Ball(speed = 7, color = BLUE)
ball2 = Ball(700, angle = 180, speed = 3)
ball3 = Ball(400, speed = 0, color = BLACK)

escenario = Scenenary(screen, ball1, ball2, ball3, e = coefficient)


running = True
simulation_started = False
times = []
energies = []
momentums = []
collision_times = []  # List to store collision times
gameEnd = False

# Loop principal de la simulación
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else: 
            escenario.handleEvent(event)

    screen.fill(GREEN)  # Rellenamos la pantalla con el color verde

    escenario.checkCollisions()

    escenario.draw()

    pygame.draw.rect(screen, BLACK, (50, 50, WIDTH - 100, HEIGHT - 100), 2)  # Dibujamos la mesa de billar

    if not simulation_started:
        # Draw start button
        start_button_rect = pygame.Rect(700, 400, 80, 40)
        pygame.draw.rect(screen, BLACK, start_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Start", True, WHITE)
        text_rect = text.get_rect(center=start_button_rect.center)
        screen.blit(text, text_rect)

        if pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos()):
            simulation_started = True
    else:
        escenario.updateData()

    pygame.display.flip()
    clock.tick(60)

print(escenario.momentum_x)
print(escenario.momentum_y)
print(escenario.kinetic_energy)
