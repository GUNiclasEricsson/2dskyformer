# https://realpython.com/pygame-a-primer/


import random
import pygame
from pygame.locals import (
    RLEACCEL,   #
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
) 

pygame.mixer.init()
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # loads an image as a surface, takes the path as argument 
        # and .convert method optimize it for faster processing
        self.surf = pygame.image.load("assets/emoji_man_rect3.png").convert()
        # .set_colorkey method takes RGB values for the color that is gonna be transparent
        # the second argument is for run-length encoding surfaces to improve performance
        # ex. WWWWWBWWWWWBWWWWB = W4BW4BW4B
        self.surf.set_colorkey((255, 255, 254), RLEACCEL)

        # self.surf = pygame.Surface((32, 32)) # old way 
        # self.surf.fill((235, 30, 201)) # old way
        
        # gets the rectangle from the self.surf attribute and 
        # is given a kwarg for the center which sets the spawning/starting position 
        self.rect = self.surf.get_rect( center=(0, SCREEN_HEIGHT / 2))


    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            # print("K_UP")
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            # print("DOWN")
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            # print("LEFT")
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            # print("RIGHT")
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def win(self):
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH / 2, 
                SCREEN_HEIGHT / 2 - 100,
            )
        )
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("assets/emoji_enemy_rect3.png").convert()
        self.surf.set_colorkey((255, 255, 255),  RLEACCEL)
        

        # self.surf = pygame.Surface((20, 10))
        # self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 15)
        
        

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < -10:
            self.kill()



class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("assets/emoji_cloud2.png").convert()
        self.surf.set_colorkey((255, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 30, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

            

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
highscore = 0
total_score = 0
current_enemies = 0
tmp_var = -1

pygame.mixer.music.load("assets/emoji_man_song3.mp3")
pygame.mixer.music.play(loops =- 1)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)


player = Player()


enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)



# surf = pygame.Surface((50, 50))
# surf.fill((0, 0, 0))
# rect = surf.get_rect()

#screen.blit(surf, ((SCREEN_WIDTH - surf.get_width()) / 2, (SCREEN_HEIGHT - surf.get_height()) / 2))
#pygame.display.flip()

#surf_center = ((SCREEN_WIDTH - surf.get_width()) / 2, (SCREEN_HEIGHT - surf.get_height()) / 2)
#screen.blit(surf, surf_center)


running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            # print("ALL", all_sprites)
            # print("NEW", new_enemy)
            # print("ENEMIES", enemies)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            
    
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    # print(pressed_keys)
    
    enemies.update()
    clouds.update()

 
    
    screen.fill((135, 206, 250))

    for entity in all_sprites:        
        screen.blit(entity.surf, entity.rect)
    #screen.blit(player.surf, player.rect)

    
    # längd på antal aktiva sprites 0 1 2 3 2 3 
    # temp var -1 0 1 2 
    
    # om antal aktiva sprites är samma som temp var
        # lägg till ett score 
        # ta bort 1 från temp var
    
    # om antal aktiva sprites är större än temp var
        # gör temp var till antal aktiva sprites - 1
    
    
    current_enemies = len(enemies)
    if current_enemies == tmp_var:
        highscore += 1
        tmp_var -= 1
    if current_enemies > tmp_var:
        tmp_var = current_enemies - 1
    print(highscore * 10)


    # an instance/object of SysFont class, argument a string with the font and the size as an integer  
    font = pygame.font.SysFont("arial", 50)
    # a variable from the method of the "font"-object given a formated string as an argument 
    total_score = font.render(f"Score: {highscore * 10}", True, (255, 255, 0))
    # the blit method is called on the screen object given the "total_score"-variable and it's position as arguments 
    screen.blit(total_score, (SCREEN_WIDTH - SCREEN_WIDTH + 10, 10))


    if pygame.sprite.spritecollideany(player, enemies):   
        game_over = font.render(f"Your final score: {highscore * 10} ", True, (255, 255, 0))
        player.win()
        screen.blit(game_over, (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 25))
        screen.blit(player.surf, player.rect)
        pygame.display.flip()
        pygame.mixer.music.stop()
        pygame.time.delay(2000)
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
