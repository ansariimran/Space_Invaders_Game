# I tried my best to explain the things which needs to be explained; 
# I left some things which are easy & obvious according to me


import pygame
import os
import time
import random

#sometimes we call methods from imported modules beforehand so that codes run smoothly
pygame.font.init()


#settind the window for game
WIDTH, HEIGHT = 750, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Game")


# SECTION-X__Loading all the images__start
RED_SPECE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
# we could load the same image in below manner 
# RED_SPECE_SHIP = pygame.image.load(assets/pixel_ship_red_small.png)

GREEN_SPECE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPECE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPECE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Loading all the laser images
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#loading background image & scaling equal to window simultaneously
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
# SECTION-X__Loading all the images__complete

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        
    def move(self, vel):
        self.y += vel
    
    #function defining when laser is off the screen
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)

#SECTION-1
#creating class having common functionalities and attributes so that it can be inherited
class Ship:
    
    COOLDOWN = 30
 
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
            #below code was for creating rectangle instead of player ship/ships just to setup movement
            #pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50))
            
        for laser in self.lasers:
            laser.draw(window)
              
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
            
    #In This function; elif part ensures that when cool_down_counter variable is greater than zero,
    # it increases by one in each program run and "if" part ensures that as the variable gets equal to
    # constant COOLDOWN, then cool_down_counter is set to zero.
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    #following the cool_down_function, IN this function, when cool_down_counter is eqaul to zero,
    #  laser object is created and it is appended into laser list. Also Variable is set to 1     
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPECE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    ##################################################


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += SPEED

    # def shoot(self):
    #     if self.cool_down_counter == 0:
    #         laser = Laser(self.x, self.y, self.laser_img)
    #         self.lasers.append(laser)
    #         self.cool_down_counter = 1
    ##########################################

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        self.lasers.remove(laser)
                        objs.remove(obj)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
                   
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height()+10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height()+10, self.ship_img.get_width() * (self.health/self.max_health), 10))
        
class Enemy(Ship):
    
    #creating a dictionary for different color's ship and laser set;
    #so that these keys can be used in random set generation with random method.
    COLOR_MAP = {"red": (RED_SPECE_SHIP, RED_LASER), "green": (GREEN_SPECE_SHIP, GREEN_LASER), "blue": (BLUE_SPECE_SHIP, BLUE_LASER)}
    
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
            
    def move(self, vel):
        self.y += vel
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-21, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    #implementation for defining offscreen postion of enemy ship; this is different from laser offscreen method
    # beacuse if you add the condition "self.y >= 0"   then as soon as enemy ships are created 
    # they come under off screen category and you lose; you are encouraged to try

    def off_screen(self, height):
        return not(self.y <= height)
    
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x 
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


#SECTION-2
#defining a main function for getting the event type & responding accordingly
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 30)
    global SPEED
    SPEED = 1
    enemies = []  
    wave_length = 5
    enemy_vel = 1 #this dictates the unit speed of enemyShips
    laser_vel = 5
    
    player_vel = 5 #this dictates the unit speed of player
    player = Player(300, 580)
    #creating ship on the screen with instantiating class ship which is calling pygame.draw.rect() method
    #  to create rectangle for ship
    
    clock = pygame.time.Clock()
    
    lost = False
    lost_count = 0
    
    
    #SUBSECTION-21
    def redraw_window():
        WIN.blit(BG, (0,0))
        #draw text
        lives_lebel = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_lebel = main_font.render(f"Level: {level}", 1, (255,255,255))
        
        WIN.blit(lives_lebel, (10,10))
        WIN.blit(level_lebel, (WIDTH - level_lebel.get_width() - 10,10))
        
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)
        
        if lost:
            lost_lebel = lost_font.render("You Lost!!!!", 1, (255, 255, 255))
            WIN.blit(lost_lebel, (WIDTH//2 - lost_lebel.get_width()//2, 350))
        
        
        pygame.display.update()
    
    #SUBSECTION-22        
    while run:
        clock.tick(FPS)
        redraw_window() 
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
            
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            SPEED += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:     #for moving player ship to the left
            player.x -= player_vel 
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:    #for moving player ship to the right
            player.x += player_vel  
        if keys[pygame.K_w] and player.y - player_vel > 0:        #for moving player ship to the Upside
            player.y -= player_vel  
        if keys[pygame.K_z] and player.y + player_vel + player.get_height() + 15 < HEIGHT:        #for moving player ship to the downside
            player.y += player_vel    
            
        if keys[pygame.K_SPACE]:
            player.shoot()
            

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.off_screen(HEIGHT):
                enemies.remove(enemy)
                lives -= 1
        
            #if enemy.y + enemy.get_height() > HEIGHT:
             #   lives -= 1 
              #  break
            
                # enemies.remove(enemy) ; This code was causing to remove the enemy twice from the list resulting in following exception - "Exception has occurred: ValueError list.remove(x): x not in list"
                #below code-line is my own solution for resolving valueError exception
                
        player.move_lasers(-laser_vel, enemies)
 
 
 
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_lebel = title_font.render("Press any mouse button to begin", 1, (0, 0, 255))
        WIN.blit(title_lebel, (WIDTH//2 - title_lebel.get_width()//2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
                
main_menu()