import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Breakers")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

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

def main():
    clock = pygame.time.Clock()
    running = True

    paddle = Paddle(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 30, 120, 20, color=WHITE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-5) # Move left
        if keys[pygame.K_RIGHT]:
            paddle.move(5)  # Move right

        screen.fill((0, 0, 0))

        paddle.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
