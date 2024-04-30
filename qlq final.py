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

KINDS_OF_COLLISION = ['Inelastica', 'Elastica', 'Completamente inelastica']

# Clase que contiene el escenario 
class Scenenary: 
    # Constructor 
    def __init__(self, screen, kind, *balls, e = 1):
        """
            Constructor de escenario, recibe como primer argumento posicional el tipo de colision
            El resto de argumentos posicionales son las bolas que formarán parte del escenario
            y como kwargument tenemos el coeficiente de restitución por default es 1 que es una colision completamente elastica
        """
        assert(kind in KINDS_OF_COLLISION)
        self.kind = kind
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
        m = [0,0,0]
        for ball in self.balls: 
            m += ball.momentum()
        # Añadiendo valores a historial 
        self.kinetic_energy.append(k)
        self.momentum.append(m[0])
        self.momentum.append(m[1])
        self.momentum.append(m[2])
    # Método para chequear coliciones entre todas las bolas que se encuentran en el escenario
    def checkCollisions(self):
        # Chequeando por cada bola
        for ball1, ball2 in combinations(self.balls, 2):
            ball1.checkCollision(ball2, self.kind, self.e)
    # Dibujando las bolas
    def draw(self):
        for ball in self.balls:
            ball.draw(self.screen)

# Clase para representar una bola
class Ball:
    # Constructor
    def __init__(self, x = 200, y = 200, radius = 10, mass = 1, speed = 10, angle = 0, color = RED):
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
        self.mass = mass
        # Transformando ángulo obtenido a radianes (con estos funciona la libreria math de python)
        self.angle = math.radians(angle % 360)
        # Descomponiendo velocidad en ejes
        self.vy = math.sin(self.angle) * self.speed 
        self.vx = math.cos(self.angle) * self.speed

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

    # Helper que dibuja la bola en pantalla
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    # Chequeamos posible collision: 
    def checkCollision(self, other, kind, e):     
        assert(kind in KINDS_OF_COLLISION)  
        #Chequeando si están en contacto
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        # Sí no están en contacto ya sabemos que no hay collision 
        if distance > self.radius + other.radius:
            return False
        elif kind == KINDS_OF_COLLISION[2]:
            print("comp inelastica")
            # Colisión completamente inelastica
            vfx = (self.vx * self.mass + other.vx * other.mass) / (self.mass + other.mass)
            vfy = (self.vy * self.mass + other.vy * other.mass) / (self.mass + other.mass)
            # Actualizamos velocidades
            self.updateSpeed(vfx, vfy)
            other.updateSpeed(vfx, vfy)
            return True
        elif kind == KINDS_OF_COLLISION[1] or kind == KINDS_OF_COLLISION[0]:
            print("Elastica o inelastica")
            # Para colisión inelastica y elastica podemos usar las mismas formulas basadas en el coeficiente de restitución
            vfx = (self.mass * self.vx + other.mass * (other.vx + e * (other.vx - self.vx))) / (self.mass + other.mass) 
            othervfx = (self.mass * (self.vx - vfx) + other.mass * other.vx) / other.mass
            vfy = (self.mass * self.vy + other.mass * (other.vy + e * (other.vy - self.vy))) / (self.mass + other.mass)
            othervfy = (self.mass * (self.vy - vfy) + other.mass * other.vy) / other.mass
            # Actualizando velocidades
            self.updateSpeed(vfx, vfy)
            other.updateSpeed(othervfx, othervfy)
            return True


    # Método que chequea si la bola va a colicionar con una pared (no genera perdidas de energía cinetica)
    def check_boundary_collision(self):
        if self.x - self.radius <= 50 or self.x + self.radius >= WIDTH - 50:
            self.angle = math.pi - self.angle
        if self.y - self.radius <= 50 or self.y + self.radius >= HEIGHT - 50:
            self.angle = 2 * math.pi - self.angle

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Creación de las bolas (valores iniciales)
ball1 = Ball(speed = 3, color = BLUE)
ball2 = Ball(700, angle = 180, speed = 2)

escenario = Scenenary(screen, KINDS_OF_COLLISION[1], ball1, ball2, e = .05)
"""
# Inicialización de Matplotlib para la gráfica de energía cinética
plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Bola 1', color='r')
line2, = ax.plot([], [], label='Bola 2', color='b')
ax.legend()
ax.set_xlim(0, 200)
ax.set_ylim(0, 100)

# Función para mostrar el menú
def draw_menu():
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 30)

    # Título
    text = font.render("Configuración de Bolas", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    # Parámetros de la bola 1
    text = font.render("Bola 1:", True, BLACK)
    screen.blit(text, (100, 150))
    text = font.render("Tamaño:", True, BLACK)
    screen.blit(text, (100, 200))
    text = font.render("Velocidad:", True, BLACK)
    screen.blit(text, (100, 250))
    text = font.render("Ángulo:", True, BLACK)
    screen.blit(text, (100, 300))

    # Parámetros de la bola 2
    text = font.render("Bola 2:", True, BLACK)
    screen.blit(text, (WIDTH - 300, 150))
    text = font.render("Tamaño:", True, BLACK)
    screen.blit(text, (WIDTH - 300, 200))
    text = font.render("Velocidad:", True, BLACK)
    screen.blit(text, (WIDTH - 300, 250))
    text = font.render("Ángulo:", True, BLACK)
    screen.blit(text, (WIDTH - 300, 300))

    # Valores de los parámetros
    text = font.render(str(ball_radius), True, BLACK)
    screen.blit(text, (250, 200))
    text = font.render(str(ball1_speed), True, BLACK)
    screen.blit(text, (250, 250))
    text = font.render(str(ball1_angle), True, BLACK)
    screen.blit(text, (250, 300))

    text = font.render(str(ball_radius), True, BLACK)
    screen.blit(text, (WIDTH - 150, 200))
    text = font.render(str(ball2_speed), True, BLACK)
    screen.blit(text, (WIDTH - 150, 250))
    text = font.render(str(ball2_angle), True, BLACK)
    screen.blit(text, (WIDTH - 150, 300))

    # Botón de inicio
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 50, HEIGHT - 100, 100, 50))
    text = font.render("Iniciar", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))

    pygame.display.flip()

# Loop principal
configuring_balls = True
while configuring_balls:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Comprobar si se hace clic en el botón de inicio
            if WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 50:
                configuring_balls = False

    # Actualizar parámetros de las bolas según la entrada del usuario
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_radius = max(5, ball_radius - 1)
    if keys[pygame.K_RIGHT]:
        ball_radius = min(50, ball_radius + 1)
    if keys[pygame.K_UP]:
        ball1_speed = min(20, ball1_speed + 1)
    if keys[pygame.K_DOWN]:
        ball1_speed = max(1, ball1_speed - 1)
    if keys[pygame.K_a]:
        ball2_speed = min(20, ball2_speed + 1)
    if keys[pygame.K_s]:
        ball2_speed = max(1, ball2_speed - 1)
    if keys[pygame.K_w]:
        ball1_angle = (ball1_angle + 5) % 360
    if keys[pygame.K_z]:
        ball1_angle = (ball1_angle - 5) % 360
    if keys[pygame.K_o]:
        ball2_angle = (ball2_angle + 5) % 360
    if keys[pygame.K_l]:
        ball2_angle = (ball2_angle - 5) % 360

    # Actualizar las bolas con los nuevos parámetros
    ball1 = Ball(100, 300, ball_radius, RED, ball1_speed, ball1_angle)
    ball2 = Ball(300, 300, ball_radius, BLUE, ball2_speed, ball2_angle)

"""
# Loop principal de la simulación
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GREEN)  # Rellenamos la pantalla con el color verde

    escenario.updateData()

    escenario.checkCollisions()

    escenario.draw()

    pygame.draw.rect(screen, BLACK, (50, 50, WIDTH - 100, HEIGHT - 100), 2)  # Dibujamos la mesa de billar
    """
    if len(ball1.kinetic_energy) > 200:
        ball1.kinetic_energy.pop(0)
    if len(ball2.kinetic_energy) > 200:
        ball2.kinetic_energy.pop(0)
    line1.set_xdata(np.arange(len(ball1.kinetic_energy)))
    line1.set_ydata(ball1.kinetic_energy)
    line2.set_xdata(np.arange(len(ball2.kinetic_energy)))
    line2.set_ydata(ball2.kinetic_energy)
    #fig.canvas.draw()
    plt.pause(0.0001)
    """

    pygame.display.flip()
    clock.tick(60)
