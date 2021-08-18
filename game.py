# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 03:00:09 2021

@author: xinyu
"""

import pygame
import random
import os

# initialization and create windows
pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255,255,255)

width, height = 500, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Thunder Fighter 雷霆战机")


# load image: os.path return the location of the current .py file
bg_img = pygame.image.load(os.path.join("images", "bg_img.JPG")).convert()
fighter_img = pygame.image.load(os.path.join("images", "su57_img.png")).convert()
fighter_mini = pygame.transform.scale(fighter_img, (25, 25))
fighter_mini.set_colorkey(WHITE)

pygame.display.set_icon(fighter_mini)

# rock_img = pygame.image.load(os.path.join("images", "rock5.png")).convert()
bullet1_img = pygame.image.load(os.path.join("images", "bu1.PNG")).convert()
bullet2_img = pygame.image.load(os.path.join("images", "bu2.PNG")).convert()
bullet3_img = pygame.image.load(os.path.join("images", "bu3.PNG")).convert()

rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("images", f"rock{i}.png")).convert())

expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['fighter'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("images", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (70, 70)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    
    fighter_exp_img = pygame.image.load(os.path.join("images", f"player_expl{i}.png")).convert()
    fighter_exp_img.set_colorkey(BLACK)
    expl_anim['fighter'].append(fighter_exp_img)

power_imgs = {}
hp_img = pygame.image.load(os.path.join("images", "red.png")).convert()
hp_img = pygame.transform.scale(hp_img, (30, 30))
hp_img.set_colorkey(WHITE)
power_imgs['hp'] = hp_img

gun_img = pygame.image.load(os.path.join("images", "gun.png")).convert()
gun_img.set_colorkey(BLACK)
power_imgs['gun'] = gun_img
    
# load sound
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
hp_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.5)

gg_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))

# game setting
clock = pygame.time.Clock()
FPS = 60
WHITE = (255,255,255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# font_name = pygame.font.match_font('arial')
font_name = os.path.join("msjh_0.ttf")

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    # True means antialias (反锯齿)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx, text_rect.top = x, y
    surface.blit(text_surface, text_rect)
    
def new_rock():
    rock = Rock()
    all_sprites.add(rock)  
    rocks.add(rock)
    
def draw_hp(surface, hp, x, y):    
    if hp < 0: hp = 0
    bar_w, bar_h = 100, 10
    fill = (hp)/300 * bar_w
    out_rect = pygame.Rect(x, y, bar_w, bar_h)
    fill_rect = pygame.Rect(x, y, fill, bar_h)    
    pygame.draw.rect(surface, GREEN, fill_rect)
    # 2 means stroke
    pygame.draw.rect(surface, BLACK, out_rect, 2)

def draw_lives(surface, lives, img, x, y):    
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)

def draw_init():
    t1 = 'Thunder Fighter 雷霆战机'
    t2 = 'Version 1.0 - Roaring Su57'
    t3 = 'Designed and Published by Mike Yu.'
    t4 = 'All Rights Reserved.'
    t5 = 'Quick Guide: use ← and → to move, press x to shoot.'
    t6 = 'Press any key to start!'
    draw_text(screen, t1, 40, width/2, height/4)
    draw_text(screen, t2, 15, width/2, height/2)
    draw_text(screen, t3, 15, width/2, height/2 + 18)
    draw_text(screen, t4, 15, width/2, height/2 + 34)
    draw_text(screen, t5, 20, width/2, height * 3/4)
    draw_text(screen, t6, 30, width/2, height * 3/4 + 30)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        # get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return True
            # KEYUP means the key is pressed down and bounces back
            elif event.type == pygame.KEYUP:
                waiting = False
                return False        
# Fighter inherits pygame.sprite.Sprite
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(fighter_img, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.radius = 25
        self.speedx = 5
        self.hp = 300
        self.lives = 3
        self.hidden = False
        self.hidden_t = 0
        self.gun = 1
        self.gun_t = 0
    def update(self):
        now = pygame.time.get_ticks()
        if self.gun >= 2 and now - self.gun_t > 5000:
            self.gun -= 1
            self.gun_t = now
            if self.gun < 1: self.gun == 1
        # 1000 is for 1000 ms
        if self.hidden and now - self.hidden_t > 1000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]: self.rect.x += self.speedx
        if key[pygame.K_LEFT]: self.rect.x -= self.speedx
        
        if self.rect.right > width: self.rect.right = width
        if self.rect.left < 0: self.rect.left = 0
    def shoot(self):
        if not self.hidden:
            if self.gun == 1:
                bullet = Bullet1(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun == 2:
                bullet1 = Bullet1(self.rect.centerx, self.rect.top)
                bullet2 = Bullet2(self.rect.left, self.rect.top)
                bullet3 = Bullet2(self.rect.right, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
            elif self.gun >= 3:
                bullet1 = Bullet1(self.rect.centerx, self.rect.top)
                bullet2 = Bullet2(self.rect.left, self.rect.top)
                bullet3 = Bullet2(self.rect.right, self.rect.top)
                bullet4 = Bullet3(self.rect.left - 20, self.rect.top)
                bullet5 = Bullet3(self.rect.right + 20, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                all_sprites.add(bullet5)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                bullets.add(bullet5)
                shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hidden_t = pygame.time.get_ticks()
        # hide the fighter: remove the fighter outside the window
        self.rect.center = (width/2, height+500)
    def gun_up(self):
        self.gun += 1
        self.gun_t = pygame.time.get_ticks()        

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(rock_imgs)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width-self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.radius = 22
        self.speedy = random.randrange(3, 6)
        self.speedx = random.randrange(-2, 2)
        self.total_degree = 0
        self.degree = random.randrange(-3, 3)
        
    def rotate(self):
        self.total_degree += self.degree
        self.total_degree = self.total_degree % 360
        # every time we rotate the original image, not the "previous" image
        self.image = pygame.transform.rotate(self.image_original, self.total_degree)
        # relocate the rock with the same center
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.rotate()
        # reset everything
        if self.rect.top > height or self.rect.left > width or self.rect.right < 0:
            self.rect.x = random.randrange(0, width-self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 6)
            self.speedx = random.randrange(-10, 10)
        
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, f_x, f_y):
        pygame.sprite.Sprite.__init__(self)       
        self.image = pygame.transform.scale(bullet1_img, (22, 60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = f_x
        self.rect.bottom = f_y - 5
        self.speedy = -8
    def update(self):
        self.rect.y += self.speedy
        # check the whole sprite group, remove this bullet for all
        if self.rect.bottom < 0: self.kill()
        
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, f_x, f_y):
        pygame.sprite.Sprite.__init__(self)       
        self.image = pygame.transform.scale(bullet2_img, (22, 60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = f_x
        self.rect.bottom = f_y - 5
        self.speedy = -8
    def update(self):
        self.rect.y += self.speedy
        # check the whole sprite group, remove this bullet for all
        if self.rect.bottom < 0: self.kill()
        
class Bullet3(pygame.sprite.Sprite):
    def __init__(self, f_x, f_y):
        pygame.sprite.Sprite.__init__(self)       
        self.image = pygame.transform.scale(bullet3_img, (22, 60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = f_x
        self.rect.bottom = f_y - 5
        self.speedy = -8
    def update(self):
        self.rect.y += self.speedy
        # check the whole sprite group, remove this bullet for all
        if self.rect.bottom < 0: self.kill()

class Explo(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)  
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        # time
        self.last_update = pygame.time.get_ticks()
        # rate
        self.frame_rate = 60
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now 
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)  
        self.type = random.choice(['hp', 'gun'])
        self.image = power_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
    def update(self):
        self.rect.y += self.speedy
        # check the whole sprite group, remove this bullet for all
        if self.rect.top > height: self.kill()
        
# sprite group
all_sprites = pygame.sprite.Group()
fighter = Fighter()
all_sprites.add(fighter)

rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
  
for i in range(10):
    new_rock()

powers = pygame.sprite.Group()

score = 0

# -1 means infinite # of plays
pygame.mixer.music.play(-1)

# game loop
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close: break
    
        show_init = False
    '''
    clock.tick(FPS) means the command (also the loop) can only be executed FPS times 
    in 1 second. We use this command to balance the difference of user devices.
    '''
    clock.tick(FPS)
    # get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                fighter.shoot()
    
                
    # update
    all_sprites.update()
    # first True: kill rock; second True: kill bullet
    collides = pygame.sprite.groupcollide(rocks, bullets, True, True)
    # recreate a rock after each collide, no need for bullet
    
    # collides is a dict{}: k for the rock, v for the bullet
    for collide in collides:
        random.choice(expl_sounds).play()
        new_rock()
        score += collide.radius * 10
        expl = Explo(collide.rect.center, 'lg')
        all_sprites.add(expl)
        # random.random returns value from 0 to 1
        if random.random() > 0.75:
            power = Power(collide.rect.center)
            all_sprites.add(power)
            powers.add(power)
    
    # Default: use rect to determine collide
    # True/False to determine whether kill the rock
    collides = pygame.sprite.spritecollide(fighter, rocks, True, pygame.sprite.collide_circle)
    
    # collides is a list[]: contains all rocks which hit the fighter
    for collide in collides:
        new_rock()
        fighter.hp -= collide.radius
        expl = Explo(collide.rect.center, 'sm')
        all_sprites.add(expl)
        if fighter.hp <= 0: 
            gg = Explo(fighter.rect.center, 'fighter')
            all_sprites.add(gg)
            gg_sound.play()
            fighter.lives -= 1
            fighter.hp = 300
            fighter.hide()
            
    collides = pygame.sprite.spritecollide(fighter, powers, True)
    for collide in collides:
        if collide.type == 'hp':
            fighter.hp += 50
            if fighter.hp >= 300: fighter.hp = 300
            hp_sound.play()
        if collide.type == 'gun':
            fighter.gun_up()
            gun_sound.play()
    
    # gg.alive() determines whether gg is still alive
    if fighter.lives == 0 and not(gg.alive()): running = False
    
    # display
    screen.fill(BLACK)
    screen.blit(bg_img, (-width/2, -height/2))
    all_sprites.draw(screen)
    text = "score: " + str(score)
    draw_text(screen, text, 25, width/2, 10)
    draw_hp(screen, fighter.hp, 5, 10)
    draw_lives(screen, fighter.lives, fighter_mini, width - 100, 15)
    
    pygame.display.update()

pygame.quit()
























