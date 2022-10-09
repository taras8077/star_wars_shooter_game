#Створи власний Шутер!

from pygame import *
from random import randint
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound=mixer.Sound("fire.ogg")
img_back="galaxy.jpg"
img_X_WING="X_WING_2.png"
img_Enemy="TIE_FIGHTER.png"
font.init()
font1=font.SysFont("Arial",60)
font2=font.SysFont("Arial",40)
score=0
goal=25
lost=0
max_lost=3
life=3
win=font1.render("Republick win",True,(255,0,0))
lose=font1.render("Empire win",True,(125.7,125.7,125.7))
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        mw.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_d] and self.rect.x<620:
            self.rect.x+=self.speed
    def fire(self):
        bullet=Bullet("laser6.png",self.rect.centerx,self.rect.top,5,25,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>win_height:
            self.rect.x=randint(80,620)
            self.rect.y=0
            lost=lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y < 0:
            self.kill()

win_width=700
win_height=500
display.set_caption("shooter")
mw=display.set_mode((win_width,win_height))
background=transform.scale(image.load(img_back),(win_width,win_height))
X_Wing=Player(img_X_WING,5,350,80,80,10)
bullets=sprite.Group()
monsters=sprite.Group()
for i in range(1,6):
    monster=Enemy(img_Enemy,randint(60,620),-40,55,85,randint(1,5))
    monsters.add(monster)
asteroids=sprite.Group()
for i in range(1,3):
    asteroid=Enemy("asteroid.png",randint(80,620),-40,80,50,randint(1,3))
    asteroids.add(asteroid)
run=True
finish=False
rel_time=False
num_fire=0
from time import time as timer
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                if num_fire<16 and rel_time==False:
                    num_fire+=1
                    fire_sound.play( )
                    X_Wing.fire()
                if num_fire>=16 and rel_time==False:
                    rel_time=True
                    last_time=timer()
    if not finish:
        mw.blit(background,(0,0))

        X_Wing.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        X_Wing.reset()
        monsters.draw(mw)
        bullets.draw(mw)
        asteroids.draw(mw)
        if rel_time==True:
            now_time=timer()
            if now_time-last_time<6:
                reload=font2.render("the gun overheated",1,(155,10,10))
                mw.blit(reload,(260,460))
            else:
                num_fire=0
                rel_time=False
        colides=sprite.groupcollide(monsters,bullets,True,True)
        for c in colides:
            score=score+1
            monster=Enemy(img_Enemy,randint(60,620),-40,55,85,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(X_Wing ,monsters,False)or sprite.spritecollide(X_Wing,asteroids,False):
            sprite.spritecollide(X_Wing,monsters,True)
            sprite.spritecollide(X_Wing,asteroids,True)
            life=life-1
        if life==0 or lost>=max_lost:
            finish=True
            mw.blit(lose,(200,200))
        if score>=goal:
            finish=True
            mw.blit(win,(200,200))
        if life==3:
            color_life=(0,150,0)
        if life==2:
            color_life=(100,150,0)
        if life==1:
            color_life=(150,0,0)
        text_life=font1.render(str(life),1,color_life)
        mw.blit(text_life,(650,10))
        text_lose=font1.render("Пропущено: "+str(lost),1,(255,255,255))
        mw.blit(text_lose,(10,50))
        score_text=font2.render("Score: "+str(score),1,(255,255,255))
        mw.blit(score_text,(10,20))

            

        display.update()
    else:
        finish=False
        score=0
        lost=0
        num_fire=0
        life=3
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1,6):
            monster=Enemy(img_Enemy,randint(60,620),-40,55,85,randint(1,5))
            monsters.add(monster)
        for i in range(1,3):
                asteroid=Enemy("asteroid.png",randint(80,620),-40,80,50,randint(1,3))
                asteroids.add(asteroid)    
    time.delay(50)
