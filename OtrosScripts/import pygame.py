import pygame 
import random
import math
import sys

# Inicializar pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Colisiones de Bolas")

# Clase para representar las bolas
class Ball:
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Rebotar en los bordes
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.velocity[0] *= -1
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.velocity[1] *= -1

# Función para manejar colisiones entre bolas
def collide(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < ball1.radius + ball2.radius:
        # Calcular nuevo vector de velocidad después de la colisión
        angle = math.atan2(dy, dx)
        magnitude_1 = math.sqrt(ball1.velocity[0]**2 + ball1.velocity[1]**2)
        magnitude_2 = math.sqrt(ball2.velocity[0]**2 + ball2.velocity[1]**2)

        new_x_velocity_1 = magnitude_1 * math.cos(angle)
        new_y_velocity_1 = magnitude_1 * math.sin(angle)
        new_x_velocity_2 = magnitude_2 * math.cos(angle)
        new_y_velocity_2 = magnitude_2 * math.sin(angle)

        ball1.velocity = [new_x_velocity_2, new_y_velocity_2]
        ball2.velocity = [new_x_velocity_1, new_y_velocity_1]

# Función principal para correr la simulación
def simulation(balls):
    running = True

    # Bucle principal
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar y mover las bolas
        for ball in balls:
            ball.move()
            ball.draw()

        # Verificar colisiones entre las bolas
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                collide(balls[i], balls[j])

        pygame.display.flip()

    pygame.quit()

# Función para crear bolas según la selección del usuario
def create_balls():
    balls = []
    num_balls = int(input("Ingrese el número de bolas: "))

    for _ in range(num_balls):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        radius = random.randint(10, 30)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        velocity = [random.choice([-2, 2]), random.choice([-2, 2])]
        balls.append(Ball(x, y, radius, color, velocity))

    return balls

# Función para mostrar el menú y manejar las selecciones del usuario
def menu():
    print("Seleccione el tipo de colisión:")
    print("1. Elástica")
    print("2. Inelástica")
    print("3. Totalmente inelástica")
    choice = int(input("Ingrese su elección (1/2/3): "))
    if choice not in [1, 2, 3]:
        print("Selección inválida.")
        sys.exit()

    return choice

# Iniciar el programa
if __name__ == "__main__":
    balls = create_balls()  # Crear las bolas según las selecciones del usuario
    collision_type = menu()  # Mostrar el menú y obtener el tipo de colisión

    if collision_type == 1:
        print("Colisión elástica seleccionada.")
    elif collision_type == 2:
        print("Colisión inelástica seleccionada.")
    elif collision_type == 3:
        print("Colisión totalmente inelástica seleccionada.")

    simulation(balls)  # Iniciar la simulación
