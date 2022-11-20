from pygame import *
from random import randint
from time import time as timer
mw_w = 700
mw_h = 500
mw = display.set_mode((mw_w,mw_h))
display.set_caption('Шутер')
Cl = time.Clock()
bg = transform.scale(image.load('galaxy.jpg'),(mw_w,mw_h))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self,p_image,p_speed,p_x,p_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(size_x,size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        mw.blit(self.image,(self.rect.x,self.rect.y))

class Puli(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill() 

Bullets=sprite.Group()

class PS(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Puli('plasma.png', 10, self.rect.centerx, self.rect.top, 10, 10)
        bullet.add(Bullets)
        fire.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, mw_w - 80)
            self.rect.y = 0
            global lost
            lost += 1

class Stone(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, mw_w - 80)
            self.rect.y = 0

score = 0
lost = 0
life = 3
oboima = 5
rel_time =  False

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 72)

player = PS(('ufo.png'),5,350,420, 50, 35)
stones = sprite.Group()
ufos = sprite.Group()
for i in range(1, 4):
    enemy = Enemy('ufo.png', randint(1, 3), randint(20, mw_w - 80), -40, 80, 50,)
    enemy.add(ufos)
for i in range(1, 4):
    asteroid = Stone('asteroid.png', randint(1, 4), randint(20, mw_w - 80), -40, 80, 50,)
    asteroid.add(stones)

lose = font2.render('Ты проиграл', 1, (255, 0, 0))
win = font2.render('Ты победил', 1, (0, 255, 0))
text_reload = font1.render('Перезарядка...', 1, (255, 0, 0))

finish = False
run = True
while run:
    text_lose = font1.render('Пропущено:' + str(lost), 1, (113, 31, 220))
    text_score = font1.render('Сбито:' + str(score), 1, (113, 31, 220))
    text_life = font1.render('Жизни:' + str(life), 1, (113, 31, 220))
    text_oboima = font1.render('Патроны:' + str(oboima), 1, (113, 31, 220))
    
    Cl.tick(60)
    mw.blit(bg,(0,0))
    mw.blit(text_lose,(1,1))
    mw.blit(text_score,(1,25))
    mw.blit(text_life,(1,49))
    mw.blit(text_oboima,(1,73))
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if oboima > 0 and rel_time == False:
                    player.fire()
                    oboima = oboima - 1
                if oboima <= 0 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if finish == False:
        player.reset()
        player.update()
        Bullets.draw(mw)
        Bullets.update()
        stones.draw(mw)
        stones.update()
        ufos.draw(mw)
        ufos.update()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1.5:
                mw.blit(text_reload, (260, 460))
            else:
                oboima = 5
                rel_time = False

        collides = sprite.groupcollide(ufos,Bullets, True, True)
        for i in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(1, 4), randint(20, mw_w - 80), -40, 80, 50,)
            enemy.add(ufos)
        if sprite.spritecollide(player,stones, True) or sprite.spritecollide(player,ufos, True):
            asteroid = Stone('asteroid.png', randint(1, 4), randint(20, mw_w - 80), -40, 80, 50,)
            asteroid.add(stones)
            life -= 1

        if life <= 0 or lost >= 3:
            finish = True
            mw.blit(lose, (210, 200))
        if score >= 10:
            finish = True
            mw.blit(win, (210, 200))
        display.update()
#