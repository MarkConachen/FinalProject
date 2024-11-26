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
        self.dx = 5  # Ball horizontal speed
        self.dy = 5  # Ball vertical speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

def main():
    clock = pygame.time.Clock()
    running = True

    paddle = Paddle(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 30, 120, 20, color=WHITE)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-5) # Move left
        if keys[pygame.K_RIGHT]:
            paddle.move(5)  # Move right

        ball.move()

        screen.fill((0, 0, 0))

        paddle.draw()
        ball.draw()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
