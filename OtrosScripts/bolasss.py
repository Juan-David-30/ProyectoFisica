import pygame
import math
import matplotlib.pyplot as plt

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
GRAVITY = 0  # No gravity
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Class for Ball
class Ball:
    def __init__(self, x, y, vx, vy, mass, color, radius):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color
        self.radius = radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.dragging = False
        self.dragging_arrow = False
        self.arrow_end_x = self.x
        self.arrow_end_y = self.y

    def update_rect(self):
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.line(screen, GREEN, (self.x, self.y), (self.arrow_end_x, self.arrow_end_y), 3)
        pygame.draw.circle(screen, GREEN, (int(self.arrow_end_x), int(self.arrow_end_y)), 5)

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

# Function to handle collisions between balls
def handle_collisions(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance < 2 * ball1.radius:
        normal_x = dx / distance
        normal_y = dy / distance
        tangent_x = -normal_y
        tangent_y = normal_x

        # Project velocities onto normal and tangent directions
        v1n = ball1.vx * normal_x + ball1.vy * normal_y
        v1t = ball1.vx * tangent_x + ball1.vy * tangent_y
        v2n = ball2.vx * normal_x + ball2.vy * normal_y
        v2t = ball2.vx * tangent_x + ball2.vy * tangent_y

        # Calculate new normal velocities after collision
        m1 = ball1.mass
        m2 = ball2.mass
        u1 = ((m1 - m2) * v1n + 2 * m2 * v2n) / (m1 + m2)
        u2 = ((m2 - m1) * v2n + 2 * m1 * v1n) / (m1 + m2)

        # Update velocities
        ball1.vx = u1 * normal_x + v1t * tangent_x
        ball1.vy = u1 * normal_y + v1t * tangent_y
        ball2.vx = u2 * normal_x + v2t * tangent_x
        ball2.vy = u2 * normal_y + v2t * tangent_y

# Function to update balls
def update_balls(ball1, ball2):
    ball1.x += ball1.vx
    ball1.y += ball1.vy
    ball1.update_rect()  # Update rect position
    ball2.x += ball2.vx
    ball2.y += ball2.vy
    ball2.update_rect()  # Update rect position

# Function to plot energy and momentum
def plot_data(times, energies, momentums, collision_times):
    plt.subplot
    (2, 1, 1)
    plt.plot(times, energies)
    plt.title('Kinetic Energy')
    plt.xlabel('Time')
    plt.ylabel('Energy')
    plt.grid(True)
    for col_time in collision_times:
        plt.axvline(x=col_time, color='r', linestyle='--')

    plt.subplot(2, 1, 2)
    plt.plot(times, momentums)
    plt.title('Momentum')
    plt.xlabel('Time')
    plt.ylabel('Momentum')
    plt.grid(True)
    for col_time in collision_times:
        plt.axvline(x=col_time, color='r', linestyle='--')

    plt.tight_layout()
    plt.pause(0.01)  # Pause to update the plot

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Collision Simulation")
clock = pygame.time.Clock()

# Create balls
ball1 = Ball(WIDTH // 4, HEIGHT // 2, 4, 0, 1, RED, BALL_RADIUS)
ball2 = Ball(3 * WIDTH // 4, HEIGHT // 2, -4, 0, 1, BLUE, BALL_RADIUS)

# Variables
running = True
simulation_started = False
times = []
energies = []
momentums = []
collision_times = []  # List to store collision times
gameEnd = False

# Main loop
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameEnd = True
        else: 
            ball2.handle_events(event)
            ball1.handle_events(event)
    if gameEnd:
        break
    # Update simulation
    if simulation_started:
        update_balls(ball1, ball2)
        handle_collisions(ball1, ball2)

        # Calculate and record energy and momentum
        total_energy = 0.5 * (ball1.mass * (ball1.vx ** 2 + ball1.vy ** 2) + ball2.mass * (ball2.vx ** 2 + ball2.vy ** 2))
        energies.append(total_energy)
        total_momentum = ball1.mass * math.sqrt(ball1.vx ** 2 + ball1.vy ** 2) + ball2.mass * math.sqrt(ball2.vx ** 2 + ball2.vy ** 2)
        momentums.append(total_momentum)
        times.append(pygame.time.get_ticks() / 1000)  # Convert milliseconds to seconds

        # Check for collisions and record collision times
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < 2 * ball1.radius:
            collision_times.append(times[-1])

        # Plot energy and momentum
        #plot_data(times, energies, momentums, collision_times)

    # Draw balls
    ball1.draw(screen)
    ball2.draw(screen)

    # Draw start button
    start_button_rect = pygame.Rect(700, 400, 80, 40)
    pygame.draw.rect(screen, BLACK, start_button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Start", True, WHITE)
    text_rect = text.get_rect(center=start_button_rect.center)
    screen.blit(text, text_rect)

    # Check if start button is clicked
    if not simulation_started and pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos()):
        simulation_started = True

    pygame.display.flip()
    clock.tick(FPS)
