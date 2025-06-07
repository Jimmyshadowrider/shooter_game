#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

score = 0
miss = 0
life = 100
num_fire = 0
rel_time = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
    
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < w_width-80:
            self.rect.x += self.speed

    def fire(self):
        global bullets
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -30)
        bullets.add(bullet)

    def bomb_deploy(self):
        global bombs
        bomb = Bullet('Bomb.png',self.rect.x, self.rect.top, 100, 100, -50)
        bombs.add(bomb)

        


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y >= w_height:
            self.rect.y = 0
            self.rect.x = randint(80, w_width-80)
            miss += 1
    
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= w_height:
            self.rect.y = 0
            self.rect.x = randint(80, w_width-80)
            

class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()
        


w_width = 700
w_height = 500
window = display.set_mode((w_width,w_height))

display.set_caption('Alien')

bg = transform.scale(image.load("galaxy.jpg"),(w_width  ,w_height))

ship = Player('rocket.png',w_width - 250 ,w_height - 100, 80,100,10)

aliens = sprite.Group()
for i in range(5):
    alien = Enemy('ufo.png', randint(80, w_width-80), 0, 80, 50, randint(1,5))
    aliens.add(alien)


rocks = sprite.Group()
for i in range(3):
    rock = Asteroid('asteroid.png',randint(30, w_width-30),0,80,50,randint(1,7))
    rocks.add(rock)

bullets =  sprite.Group()
bombs = sprite.Group()

font.init()
# style = font.Font(None, 36)
style = font.SysFont("Arial", 36)
# font_2 = font.Font(None, 60)
font_2 = font.SysFont("Arial", 60)
# font_1 = font.Font(None, 80)
font_1 = font.SysFont("Arial", 80)
win = font_1.render("YOU WIN", True, (255,215,0))
lose = font_1.render("YOU LOSE", True, (255,0,0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
b_sound = mixer.Sound("fire.ogg")

run = True
finish = False
clock = time.Clock()
FPS = 10
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_r:
                if num_fire < 3 and rel_time == False:
                    ship.bomb_deploy()
                    b_sound.play()
                    num_fire += 1
                if num_fire >= 3 and rel_time == False:
                    rel_time = True
                    last_time = timer()
            if e.key == K_SPACE:
                ship.fire()
                b_sound.play()

    if finish == False:
        window.blit(bg,(0,0))
        
        ship.update()
        aliens.update()
        rocks.update()
        bullets.update()
        bombs.update()
        aliens.draw(window)
        bullets.draw(window)
        bombs.draw(window)
        rocks.draw(window)
        ship.reset()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time >= 3:
                rel_time = False
                num_fire = 0
            else:
                window.blit(text_reload,(200,w_height - 50))
                
        


        collides = sprite.groupcollide(aliens, bullets, True, True)
        collided = sprite.groupcollide(aliens, bombs, True, False)
        collide_1 = sprite.groupcollide(rocks, bombs, True, True)
        for c in collides:
            score += 1
            alien = Enemy('ufo.png', randint(80, w_width-80), 0, 80, 50, randint(1,5))
            aliens.add(alien)
        for c in collided:
            score += 1
            alien = Enemy('ufo.png', randint(80, w_width-80), 0, 80, 50, randint(1,5))
            aliens.add(alien)
        for i in collide_1:
            rock = Asteroid('asteroid.png', randint(30, w_width-30), 0, 80, 50, randint(1,7))
            rocks.add(rock)
        if score >= 50:
            window.blit(win,(200, 200))
            finish = True
        if sprite.spritecollide(ship, aliens, False) or sprite.spritecollide(ship, rocks, False):
            # window.blit(lose, (200,200))
            # finish = True
            life -= 1
        if life <= 0 or miss >= 3:
            window.blit(lose, (200,200))
            finish = True

        sprite.groupcollide(rocks, bullets, False, True)
        

        text_score = style.render('Score: ' + str(score), 1, (255,255,255))
        text_miss = style.render('Missed: ' + str(miss), 1, (255,255,255))
        text_life = font_2.render(str(life), 1, (255,255,255))
        text_reload = style.render('Wait, reload...',1 ,(150,0,0))
       

        window.blit(text_miss,(10,50))
        window.blit(text_score,(10,20))
        window.blit(text_life,(w_width - 100,20))

        display.update()


 

    
     


    
    
    
    
    # clock.tick(FPS)
    time.delay(50)
    
    
    
    
    
    
    
    
    
    
    
    
