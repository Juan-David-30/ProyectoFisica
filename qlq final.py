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

# Creación de las bolas (valores iniciales)
ball_radius = 20
ball1_speed = 5
ball2_speed = 3
ball1_angle = 45
ball2_angle = 135
ball1 = Ball(100, 300, ball_radius, RED, ball1_speed, ball1_angle)
ball2 = Ball(300, 300, ball_radius, BLUE, ball2_speed, ball2_angle)

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

# Loop principal de la simulación
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GREEN)  # Rellenamos la pantalla con el color verde

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
    plt.pause(0.001)

    pygame.display.flip()
    clock.tick(60)
