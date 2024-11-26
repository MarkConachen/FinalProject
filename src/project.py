import pygame
import random
from PIL import Image

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Breakers")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BLOCK_COLOR_LEVEL_1 = (255, 165, 0)
BLOCK_COLOR_LEVEL_2 = (0, 255, 255)
BLOCK_COLOR_LEVEL_3 = (255, 0, 255)
BLOCK_COLOR_LEVEL_4 = (255, 0, 0)
BLOCK_COLOR_UNBREAKABLE = (128, 128, 128)

BLOCK_POINTS_LEVEL_1 = 10
BLOCK_POINTS_LEVEL_2 = 20
BLOCK_POINTS_LEVEL_3 = 30
BLOCK_POINTS_LEVEL_4 = 40
BLOCK_POINTS_UNBREAKABLE = 0

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.original_width = width
        self.enlarged = False
        self.enlarge_time = 10000

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, x_change):
        self.rect.x += x_change
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def enlarge(self):
        self.rect.width *= 1.4
        self.enlarged = True
        self.enlarge_time = pygame.time.get_ticks()

    def reset_size(self):
        self.rect.width = self.original_width
        self.enlarged = False

    def update(self):
        if self.enlarged and pygame.time.get_ticks() - self.enlarge_time > 10000: # 10 seconds
            self.reset_size()

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = random.choice([-4, 4])
        self.dy = -4

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.dx *= -1 # Reverse horizontal direction on impact

        if self.y - self.radius <= 0:
            self.dy *= -1 # Reverse vertical direction on impact

        if self.y + self.radius >= SCREEN_HEIGHT:
            return False
        return True

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

    def impacts_with_paddle(self, paddle):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        return ball_rect.colliderect(paddle.rect)

    def impacts_with_block(self, block):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        return ball_rect.colliderect(block.rect)

class Block:
    def __init__(self, x, y, width, height, color, point_value, destructible=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.point_value = point_value
        self.destructible = destructible

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def impacts_with_ball(self, ball):
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
        return ball_rect.colliderect(self.rect)

def get_paddle_color(level):
    if level == 1:
        return WHITE
    elif level == 2:
        return BLUE
    elif level == 3:
        return RED
    else:
        return WHITE
    
def draw_score(score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

class PowerUp:
    def __init__(self, x, y, powerup_type):
        if powerup_type == 'enlarge':
            pil_image = Image.open("powerup2.png").convert("RGBA")
        else:
            pil_image = Image.open("powerup1.png").convert("RGBA")
        
        pil_image = pil_image.resize((45, 45), Image.Resampling.LANCZOS)
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()

        self.image = pygame.image.fromstring(data, size, mode)
        self.rect = self.image.get_rect(center=(x, y))
        self.dy = 4
        self.powerup_type = powerup_type

    def move(self):
        self.rect.y += self.dy

    def draw(self):
        screen.blit(self.image, self.rect)

    def impacts_with_paddle(self, paddle):
        return self.rect.colliderect(paddle.rect)

def create_level_from_file(level_file):
    blocks = []
    block_width = 56.5
    block_height = 17.5
    x_offset = 10
    y_offset = 50
    block_spacing = 5.4

    try:
        with open(level_file, 'r') as file:
            rows = file.readlines()

        for row_idx, row in enumerate(rows):
            for col_idx, char in enumerate(row.strip()):
                if char == '1':
                    blocks.append(Block(
                        col_idx * (block_width + block_spacing) + x_offset,
                        row_idx * (block_height + block_spacing) + y_offset,
                        block_width, block_height,
                        BLOCK_COLOR_LEVEL_1, BLOCK_POINTS_LEVEL_1
                    ))
                elif char == '2':
                    blocks.append(Block(
                        col_idx * (block_width + block_spacing) + x_offset,
                        row_idx * (block_height + block_spacing) + y_offset,
                        block_width, block_height,
                        BLOCK_COLOR_LEVEL_2, BLOCK_POINTS_LEVEL_2
                    ))
                elif char == '3':
                    blocks.append(Block(
                        col_idx * (block_width + block_spacing) + x_offset,
                        row_idx * (block_height + block_spacing) + y_offset,
                        block_width, block_height,
                        BLOCK_COLOR_LEVEL_3, BLOCK_POINTS_LEVEL_3
                    ))
                if char == '4':
                    blocks.append(Block(
                        col_idx * (block_width + block_spacing) + x_offset,
                        row_idx * (block_height + block_spacing) + y_offset,
                        block_width, block_height,
                        BLOCK_COLOR_LEVEL_4, BLOCK_POINTS_LEVEL_4
                    ))
                elif char == 'U': # Letter for unbreakable block
                    blocks.append(Block(
                        col_idx * (block_width + block_spacing) + x_offset,
                        row_idx * (block_height + block_spacing) + y_offset,
                        block_width, block_height,
                        BLOCK_COLOR_UNBREAKABLE, BLOCK_POINTS_UNBREAKABLE, destructible=False
                    ))
        return blocks
    except FileNotFoundError:
        print(f"Level file {level_file} not found.")
        return []

def main():
    clock = pygame.time.Clock()
    level = 1
    max_levels = 4
    running = True
    score = 0

    paddle = Paddle(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 30, 120, 20, color=WHITE)
    balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10)]
    blocks = create_level_from_file(f"level{level}.txt")
    powerups = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        if not balls:
            running = False
            game_over(score)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-5) # Move left
        if keys[pygame.K_RIGHT]:
            paddle.move(5)  # Move right

        paddle.update()

        for ball in balls[:]:
            if not ball.move():
                balls.remove(ball)

            if ball.impacts_with_paddle(paddle):
                ball.dy *= -1

            for block in blocks[:]:
                if ball.impacts_with_block(block):
                    ball.dy *= -1
                    if block.destructible:
                        blocks.remove(block)
                        score += block.point_value
                        if random.random() < 0.2:
                            powerup_type = random.choice(['enlarge', 'extra_ball'])
                            powerups.append(PowerUp(block.rect.centerx, block.rect.centery, powerup_type))

        for powerup in powerups[:]:
            powerup.move()
            if powerup.impacts_with_paddle(paddle):
                if powerup.powerup_type == 'enlarge':
                    paddle.enlarge()
                elif powerup.powerup_type == 'extra_ball':
                    new_ball1 = Ball(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 10)
                    new_ball2 = Ball(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, 10)
                    balls.append(new_ball1)
                    balls.append(new_ball2)
                powerups.remove(powerup)

            if powerup.rect.top > SCREEN_HEIGHT:
                powerups.remove(powerup)

        remaining_blocks = [block for block in blocks if block.destructible]
        if len(remaining_blocks) == 0:
            if level < max_levels:
                level += 1
                powerups.clear()
                balls.clear()

                balls.append(Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10))
                paddle = Paddle(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 30, 120, 20, color=WHITE)
                blocks = create_level_from_file(f"level{level}.txt")
                
                pygame.time.wait(500) # Half a second pause between stages
            else:
                running = False
                game_over(score)

        screen.fill((10, 10, 10))
        paddle.draw()
        for ball in balls:
            ball.draw()
        for block in blocks:
            block.draw()
        for powerup in powerups:
            powerup.draw()

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

def game_over(score):
    print(f"Game Over! Final Score: {score}")
    
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over!", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)

    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    pygame.time.wait(5000)

if __name__ == "__main__":
    main()
