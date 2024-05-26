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

# Clase para representar una bola
class Ball:
    def __init__(self, x, y, radius, color, speed, angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.angle = angle
        self.kinetic_energy = []

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.kinetic_energy.append(0.5 * self.speed**2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def check_boundary_collision(self):
        if self.x - self.radius <= 50 or self.x + self.radius >= WIDTH - 50:
            self.angle = 180 - self.angle
        if self.y - self.radius <= 50 or self.y + self.radius >= HEIGHT - 50:
            self.angle = 360 - self.angle

def collide(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance <= ball1.radius + ball2.radius:
        tangent = math.atan2(dy, dx)
        angle1 = 2 * tangent - ball1.angle
        angle2 = 2 * tangent - ball2.angle

        speed1 = ball2.speed
        speed2 = ball1.speed

        ball1.speed = speed1
        ball2.speed = speed2

        ball1.angle = math.degrees(angle1)
        ball2.angle = math.degrees(angle2)

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Creación de las bolas
ball1 = Ball(100, 300, 20, RED, 5, 45)
ball2 = Ball(300, 300, 30, BLUE, 3, 135)

# Inicialización de Matplotlib para la gráfica de energía cinética
plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Bola 1', color='r')
line2, = ax.plot([], [], label='Bola 2', color='b')
ax.legend()
ax.set_xlim(0, 200)
ax.set_ylim(0, 100)

# Loop principal
while True:
    screen.fill(GREEN)  # Rellenamos la pantalla con el color verde

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball1.update()
    ball2.update()

    ball1.check_boundary_collision()
    ball2.check_boundary_collision()

    collide(ball1, ball2)

    ball1.draw(screen)
    ball2.draw(screen)

    pygame.draw.rect(screen, BLACK, (50, 50, WIDTH - 100, HEIGHT - 100), 2)  # Dibujamos la mesa de billar

    if len(ball1.kinetic_energy) > 200:
        ball1.kinetic_energy.pop(0)
    if len(ball2.kinetic_energy) > 200:
        ball2.kinetic_energy.pop(0)

    line1.set_xdata(np.arange(len(ball1.kinetic_energy)))
    line1.set_ydata(ball1.kinetic_energy)
    line2.set_xdata(np.arange(len(ball2.kinetic_energy)))
    line2.set_ydata(ball2.kinetic_energy)
    fig.canvas.draw()
    fig.canvas.flush_events()

    pygame.display.flip()
    clock.tick(60)
