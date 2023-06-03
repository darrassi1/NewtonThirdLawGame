import pygame
import sys
import random

# Define the Ball class
class Ball:
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.position = [x, y]
        self.velocity = [vx, vy]
        self.force = [0, 0]

    def apply_force(self, force):
        self.force = force

    def update(self, dt):
        acceleration = [self.force[0] / self.mass, self.force[1] / self.mass]
        self.velocity[0] += acceleration[0] * dt  # Update the x-velocity
        self.velocity[1] += acceleration[1] * dt  # Update the y-velocity
        self.position[0] += self.velocity[0] * dt  # Update the x-position
        self.position[1] += self.velocity[1] * dt  # Update the y-position

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Newton's Third Law Game")

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ARROW_COLOR = (255, 255, 255)

# Set up the balls
ball_radius = 20
ball_a = Ball(1, screen_width // 4, screen_height // 2, 0, 0)  # Mass = 1, initial position = (screen_width // 4, screen_height // 2), initial velocity = (0, 0)
ball_b = Ball(1, 3 * screen_width // 4, screen_height // 2, 0, 0)  # Mass = 1, initial position = (3 * screen_width // 4, screen_height // 2), initial velocity = (0, 0)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check for keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_a.apply_force([-10, 0])  # Apply a force to the left for ball A
    elif keys[pygame.K_RIGHT]:
        ball_a.apply_force([10, 0])  # Apply a force to the right for ball A
    elif keys[pygame.K_UP]:
        ball_a.apply_force([0, -10])  # Apply a force upward for ball A
    elif keys[pygame.K_DOWN]:
        ball_a.apply_force([0, 10])  # Apply a force downward for ball A

    # Update the positions and velocities of both balls
    dt = 0.1
    ball_a.update(dt)
    ball_b.update(dt)

    # Check for collision between the balls
    distance = ((ball_a.position[0] - ball_b.position[0]) ** 2 + (ball_a.position[1] - ball_b.position[1]) ** 2) ** 0.5
    if distance <= 2 * ball_radius:  # If the balls touch or overlap
        # Swap velocities to simulate the reaction force
        ball_a.velocity[0], ball_b.velocity[0] = ball_b.velocity[0], ball_a.velocity[0]
        ball_a.velocity[1], ball_b.velocity[1] = ball_b.velocity[1], ball_a.velocity[1]

    # Prevent the balls from exceeding the screen boundaries
    if ball_a.position[0] - ball_radius <= 0:
        ball_a.position[0] = ball_radius
        ball_a.velocity[0] = 0
    if ball_a.position[0] + ball_radius >= screen_width:
        ball_a.position[0] = screen_width - ball_radius
        ball_a.velocity[0] = 0
    if ball_a.position[1] - ball_radius <= 0:
        ball_a.position[1] = ball_radius
        ball_a.velocity[1] = 0
    if ball_a.position[1] + ball_radius >= screen_height:
        ball_a.position[1] = screen_height - ball_radius
        ball_a.velocity[1] = 0
    if ball_b.position[0] - ball_radius <= 0:
        ball_b.position[0] = ball_radius
        ball_b.velocity[0] = 0
    if ball_b.position[0] + ball_radius >= screen_width:
        ball_b.position[0] = screen_width - ball_radius
        ball_b.velocity[0] = 0
    if ball_b.position[1] - ball_radius <= 0:
        ball_b.position[1] = ball_radius
        ball_b.velocity[1] = 0
    if ball_b.position[1] + ball_radius >= screen_height:
        ball_b.position[1] = screen_height - ball_radius
        ball_b.velocity[1] = 0

    # Random movement for the green ball
    random_force = [random.uniform(-5, 5), random.uniform(-5, 5)]
    ball_b.apply_force(random_force)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the balls
    pygame.draw.circle(screen, RED, (int(ball_a.position[0]), int(ball_a.position[1])), ball_radius)
    pygame.draw.circle(screen, GREEN, (int(ball_b.position[0]), int(ball_b.position[1])), ball_radius)

    # Draw arrows to indicate the forces on the balls
    arrow_scale = 10
    arrow_length = ((ball_a.force[0] ** 2 + ball_a.force[1] ** 2) ** 0.5) * arrow_scale  # Determine arrow length based on force magnitude
    arrow_x = ball_a.position[0] + ball_radius + arrow_length if ball_a.force[0] >= 0 else ball_a.position[0] - ball_radius - arrow_length
    arrow_y = ball_a.position[1] + arrow_length if ball_a.force[1] >= 0 else ball_a.position[1] - arrow_length
    pygame.draw.line(screen, ARROW_COLOR, (ball_a.position[0], ball_a.position[1]), (arrow_x, ball_a.position[1]), 2)
    pygame.draw.line(screen, ARROW_COLOR, (ball_a.position[0], ball_a.position[1]), (ball_a.position[0], arrow_y), 2)

    # Draw a line between the balls to represent the interaction
    pygame.draw.line(screen, ARROW_COLOR, (int(ball_a.position[0]), int(ball_a.position[1])), (int(ball_b.position[0]), int(ball_b.position[1])), 2)

    # Add some text to provide instructions and information
    font = pygame.font.Font(None, 30)
    instructions_text = font.render("Use arrow keys to apply forces to the red ball", True, ARROW_COLOR)
    third_law_text = font.render("Third Law of Motion: Every action has an equal and opposite reaction", True, ARROW_COLOR)
    screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, 20))
    screen.blit(third_law_text, (screen_width // 2 - third_law_text.get_width() // 2, 50))

    # Update the display
    pygame.display.update()
