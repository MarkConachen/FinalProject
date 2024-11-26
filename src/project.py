import pygame

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

BLOCK_POINTS_LEVEL_1 = 10
BLOCK_POINTS_LEVEL_2 = 20
BLOCK_POINTS_LEVEL_3 = 30

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, x_change):
        self.rect.x += x_change
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = 4.5  # Ball horizontal speed
        self.dy = 5  # Ball vertical speed

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

class Block:
    def __init__(self, x, y, width, height, color, point_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.point_value = point_value

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def impacts_with_ball(self, ball):
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
        return ball_rect.colliderect(self.rect)

def create_level(level):
    blocks = []
    block_width = 80
    block_height = 30

    if level == 1:
        rows = 1
        cols = 1
        block_color = BLOCK_COLOR_LEVEL_1
        point_value = BLOCK_POINTS_LEVEL_1
    elif level == 2:
        rows = 1
        cols = 1
        block_color = BLOCK_COLOR_LEVEL_2
        point_value = BLOCK_POINTS_LEVEL_2
    elif level == 3:
        rows = 5
        cols = 10
        block_color = BLOCK_COLOR_LEVEL_3
        point_value = BLOCK_POINTS_LEVEL_3

    for row in range(rows):
        for col in range(cols):
            blocks.append(Block(col * (block_width + 10) + 50, row * (block_height + 5) + 50, block_width, block_height, block_color, point_value))

    return blocks

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

def main():
    clock = pygame.time.Clock()
    level = 1
    running = True
    score = 0

    paddle = Paddle(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 30, 120, 20, color=WHITE)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10)

    blocks = create_level(level)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-5) # Move left
        if keys[pygame.K_RIGHT]:
            paddle.move(5)  # Move right

        if not ball.move():
            running = False

        if ball.impacts_with_paddle(paddle):
            ball.dy *= -1

        for block in blocks[:]:
            if block.impacts_with_ball(ball):
                ball.dy *= -1
                blocks.remove(block)
                score += block.point_value

        if len(blocks) == 0:
            level += 1
            blocks = create_level(level)
            paddle.color = get_paddle_color(level)

        screen.fill((0, 0, 0))

        paddle.draw()
        ball.draw()

        for block in blocks:
            block.draw()

        draw_score(score)
            
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
