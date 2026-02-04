import random
import pygame
import time
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Falling Rain')

BG = pygame.transform.scale(pygame.image.load('dark - 1.png'), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

RAIN_WIDTH = 10
RAIN_HEIGHT = 20
RAIN_VEL = 5

SCORE = 0
SCORE_INCREMENT = 1

FONT = pygame.font.SysFont("Calibri", 30)

def draw(player, elapsed_time, rains):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white')
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, 'red', player)

    for rain in rains:
        pygame.draw.rect(WIN, 'white', rain)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    rain_add_increment = 2000
    rain_count = 0
    
    rains = []
    hit = False

    while run:
        rain_count += clock.tick(144)
        elapsed_time = time.time() - start_time

        if rain_count > rain_add_increment:
            for _ in range(3):
                rain_x = random.randint(0, WIDTH - RAIN_WIDTH)
                rain = pygame.Rect(rain_x, -RAIN_HEIGHT, RAIN_WIDTH, RAIN_HEIGHT)
                rains.append(rain)
            
            rain_add_increment = max(200, rain_add_increment - 50)
            rain_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VEL
        
        for rain in rains[:]:
            rain.y += RAIN_VEL
            if rain.y > HEIGHT:
                rains.remove(rain)
            elif rain.y + RAIN_HEIGHT >= player.y and rain.colliderect(player):
                rains.remove(rain)
                hit = True
                break
        
        if hit:
            lost_text = FONT.render('You Lost!', 1, 'red')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, rains)

    pygame.quit()

if __name__ == '__main__':
    main()

