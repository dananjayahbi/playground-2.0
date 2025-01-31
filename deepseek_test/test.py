import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60

# Colors
BG_COLOR = (18, 18, 18)
SNAKE_HEAD_COLOR = (0, 230, 118)
SNAKE_BODY_COLOR = (0, 200, 100)
FOOD_COLOR = (255, 82, 82)
TEXT_COLOR = (255, 255, 255)

# Particle class for effects
class Particle:
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.lifetime = 30

    def update(self):
        self.position[0] += self.velocity[0] * 2
        self.position[1] += self.velocity[1] * 2
        self.lifetime -= 1

# Snake Game Class
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Modern Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
        
        # Particles list
        self.particles = []

    def reset_game(self):
        self.snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (0, 0)
        self.next_direction = (1, 0)  # Changed from (0, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.smooth_pos = [WIDTH//2, HEIGHT//2]

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake:
                return food

    def draw_button(self, text, position, size):
        rect = pygame.Rect(position, size)
        pygame.draw.rect(self.screen, (50, 50, 50), rect, border_radius=5)
        text_surf = self.font.render(text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        return rect

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.next_direction = (1, 0)
                else:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

    def update(self):
        if not self.game_over:
            # Update direction
            self.direction = self.next_direction
            
            # Smooth movement
            target_x = self.snake[0][0] * GRID_SIZE + GRID_SIZE//2
            target_y = self.snake[0][1] * GRID_SIZE + GRID_SIZE//2
            self.smooth_pos[0] += (target_x - self.smooth_pos[0]) * 0.2
            self.smooth_pos[1] += (target_y - self.smooth_pos[1]) * 0.2

            # Actual grid-based movement
            if (self.smooth_pos[0] - target_x)**2 + (self.smooth_pos[1] - target_y)**2 < 1:
                new_head = (
                    (self.snake[0][0] + self.direction[0]) % GRID_WIDTH,
                    (self.snake[0][1] + self.direction[1]) % GRID_HEIGHT
                )

                if new_head in self.snake:
                    self.game_over = True
                else:
                    self.snake.insert(0, new_head)
                    if new_head == self.food:
                        self.score += 1
                        self.food = self.spawn_food()
                        # Add particles
                        for _ in range(20):
                            self.particles.append(Particle((target_x, target_y)))
                    else:
                        self.snake.pop()

            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)

    def draw(self):
        self.screen.fill(BG_COLOR)

        # Draw grid lines
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (WIDTH, y))

        # Draw snake with smooth movement
        for i, segment in enumerate(self.snake):
            x = segment[0] * GRID_SIZE + GRID_SIZE//2
            y = segment[1] * GRID_SIZE + GRID_SIZE//2
            if i == 0:
                color = SNAKE_HEAD_COLOR
            else:
                color = SNAKE_BODY_COLOR
            
            # Smooth interpolation for body segments
            if i == 0:
                pos = self.smooth_pos
            else:
                prev_segment = self.snake[i-1] if i > 0 else segment
                pos = (
                    prev_segment[0] * GRID_SIZE + GRID_SIZE//2,
                    prev_segment[1] * GRID_SIZE + GRID_SIZE//2
                )
            
            # Draw snake body with gradient
            radius = GRID_SIZE//2
            for j in range(3):
                pygame.draw.circle(self.screen, 
                                 (color[0], color[1], color[2], 255 - j*50),
                                 (int(pos[0]), int(pos[1])),
                                 radius - j*2)

        # Draw food with glow effect
        food_x = self.food[0] * GRID_SIZE + GRID_SIZE//2
        food_y = self.food[1] * GRID_SIZE + GRID_SIZE//2
        for i in range(5):
            pygame.draw.circle(self.screen,
                             (FOOD_COLOR[0], FOOD_COLOR[1], FOOD_COLOR[2], 50 - i*10),
                             (food_x, food_y),
                             GRID_SIZE//2 + i*2)

        # Draw particles
        for particle in self.particles:
            alpha = particle.lifetime * 8.5
            pygame.draw.circle(self.screen,
                             (255, 255, 255, alpha),
                             (int(particle.position[0]), int(particle.position[1])),
                             2)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("Game Over!", True, TEXT_COLOR)
            self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            
            restart_text = self.font.render("Press SPACE to restart", True, TEXT_COLOR)
            self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()