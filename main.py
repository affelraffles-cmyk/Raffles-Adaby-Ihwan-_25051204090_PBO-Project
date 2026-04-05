import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")

YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 🔹 LOAD IMAGE
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (40, 40))

enemy_img = pygame.image.load("musuh2.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

bg = pygame.image.load("background.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))


class GameObject:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Player(GameObject):
    def __init__(self):
        super().__init__(300, 300, 40, (0, 0, 255))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(player_img, (self.rect.x, self.rect.y))


class Enemy(GameObject):
    def __init__(self):
        super().__init__(random.randint(0, 560), random.randint(0, 560), 40, (255, 0, 0))
        self.speed = 2

    def move(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed


    def get_hitbox(self):
        return pygame.Rect(
            self.rect.x + 10,
            self.rect.y + 10,
            20,
            20
        )

    def draw(self, screen):
        screen.blit(enemy_img, (self.rect.x, self.rect.y))


class Coin(GameObject):
    def __init__(self):
        super().__init__(random.randint(0, 560), random.randint(0, 560), 20, YELLOW)

    def respawn(self):
        self.rect.x = random.randint(0, 560)
        self.rect.y = random.randint(0, 560)


player = Player()
enemy = Enemy()
coin = Coin()

score = 0
game_over = False
running = True

while running:

    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)
        enemy.move(player)


        if player.rect.colliderect(coin.rect):
            score += 1
            coin.respawn()


        if player.rect.colliderect(enemy.get_hitbox()):
            game_over = True

    player.draw(screen)
    enemy.draw(screen)
    coin.draw(screen)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if game_over:
        text = font.render("Anda Mati", True, (0, 0, 0))
        screen.blit(text, (200, 250))

    pygame.display.update()
    clock.tick(60)

pygame.quit()