#Создай собственный Шутер!
from pygame import *
from random import randint
import random
from datetime import datetime

mixer.init()
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Papyrus', 60)
mixer.music.load('James_Liam_Figueroa_-_Gojo_s_0.2-Second_Domain_Expansion_(SkySound.cc).mp3')
mixer.music.play(-1)
clock = time.Clock()

window = display.set_mode((700, 750))
display.set_caption('Satoru vs All His Opponents')
bg = transform.scale(image.load('images-_12_.png'), (700, 750))

class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

menu_btn = GameSprite('images (1).png', 200, 170, 0, 225, 375)

class Player(GameSprite):
    def __init__(self, filename, w, h, speed, x, y, healthe=18, ammunition_1=28, ammunition_2=2):
        super().__init__(filename, w, h, speed, x, y)
        self.healthe = healthe
        self.max_healthe = healthe
        self.ammunition_type1 = ammunition_1
        self.max_ammunition_type1 = ammunition_1
        self.ammunition_type2 = ammunition_2
        self.max_ammunition_type2 = ammunition_2
        self.counter_type1 = ammunition_1
        self.counter_type2 = ammunition_2
        self.rel_time = False
        self.reload_start_time = 0
        self.reload_duration = 2000  # 2 seconds reload time
        self.buff_active = False
        self.buff_start_time = 0
        self.buff_duration = 5000
        self.original_speed = speed  # Store original speed

    def fire(self):
        global current_weapon
        if current_weapon.name == 'Красный' and self.ammunition_type1 > 0:
            bullet = Bullet('gojo red.png', 105, 135, 15, self.rect.centerx, self.rect.top, 1)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.centery = self.rect.top
            bullets.add(bullet)
            self.counter_type1 -= 1
            self.ammunition_type1 -= 1
        elif current_weapon.name == 'Фиолетовый' and self.ammunition_type2 > 0:
            bullet = Bullet('F2_xaBBXEAEvih5.png', 185, 185, 20, self.rect.centerx, self.rect.top, 2)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.centery = self.rect.top
            bullets.add(bullet)
            self.counter_type2 -= 1
            self.ammunition_type2 -= 1

    def reload(self):
        if not self.rel_time:
            self.rel_time = True
            self.reload_start_time = time.get_ticks()
            self.ammunition_type1 = self.max_ammunition_type1
            self.ammunition_type2 = self.max_ammunition_type2
            self.counter_type1 = self.ammunition_type1
            self.counter_type2 = self.ammunition_type2

    def update(self):
        keys_pressed = key.get_pressed()
        # Adjust speed during reload
        current_speed = self.original_speed / 2 if self.rel_time else self.original_speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= current_speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - 65:
            self.rect.x += current_speed
        if keys_pressed[K_r] and not self.rel_time:
            self.reload()

        if self.rel_time:
            current_time = time.get_ticks()
            if current_time - self.reload_start_time >= self.reload_duration:
                self.rel_time = False

        if self.buff_active:
            current_time = time.get_ticks()
            if current_time - self.buff_start_time <= self.buff_duration:
                elapsed_time = (current_time - self.buff_start_time) / 1000
                self.healthe = min(self.max_healthe, self.healthe + 1 * elapsed_time / self.buff_duration * 5)
                self.ammunition_type1 = min(self.max_ammunition_type1, self.ammunition_type1 + 1 * elapsed_time / self.buff_duration * 5)
                self.ammunition_type2 = min(self.max_ammunition_type2, self.ammunition_type2 + 1 * elapsed_time / self.buff_duration * 5)
                self.counter_type1 = self.ammunition_type1
                self.counter_type2 = self.ammunition_type2
            else:
                self.buff_active = False

    def apply_buff(self):
        self.buff_active = True
        self.buff_start_time = time.get_ticks()

player = Player('Без названия.png', 100, 125, 10, 300, 630)

class Enemy(GameSprite):
    def __init__(self, filename, w, h, speed, x, y, damage=2, healthe=2):
        super().__init__(filename, w, h, speed, x, y)
        self.damage = damage
        self.healthe = healthe
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 700:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.rect.w)
            lost += 1

class Boss(GameSprite):
    def __init__(self, filename, w, h, speed, x, y, damage=10000000000000000000000000000, healthe=1020):
        super().__init__(filename, w, h, speed, x, y)
        self.damage = damage
        self.healthe = healthe
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 700:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.rect.w)
            lost += 1

class Bullet(GameSprite):
    def __init__(self, filename, w, h, speed, x, y, bullet_type, damage=2):
        super().__init__(filename, w, h, speed, x, y)
        self.bullet_type = bullet_type
        self.damage = damage
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Weapon:
    def __init__(self, name, fire_rate):
        self.name = name
        self.fire_rate = fire_rate

weapons = [
    Weapon("Красный", 5),
    Weapon("Фиолетовый", 0.6),
]

class Buff(GameSprite):
    def __init__(self, x, y, duration, filename, w, h, speed):
        super().__init__(filename, w, h, speed, x, y)
        self.duration = duration
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 700:
            self.kill()

buffs = sprite.Group()
cursed = Enemy('cbbf233f1e08ab568a5e501e72948c2d (1).png', 115, 125, 2, 50, 30, 2, 2)
monsters = sprite.Group()
monsters.add(cursed)

enemies_list = [
    Enemy('Mahoraga_29.jpg', 155, 225, 1, 350, 30, 4, 6),
    Enemy('agito (1) (1) (1).png', 195, 215, 2, 150, 30, 1, 3),
    Enemy('toji.png', 120, 120, 5, 550, 30, 4, 3),
    Enemy('jogo.png', 95, 95, 3, 900, 30, 2, 5),
    Enemy('Kenjaku_29.png', 50, 125, 2, 300, 30, 5, 1)
]
monsters.add(Enemy('Mahoraga_29.jpg', 155, 225, 1, 350, 30, 4, 6))
monsters.add(Enemy('agito (1) (1) (1).png', 195, 215, 2, 150, 30, 1, 3))
monsters.add(Enemy('toji.png', 120, 120, 5, 550, 30, 4, 3))
monsters.add(Enemy('jogo.png', 95, 95, 3, 900, 30, 2, 5))
monsters.add(Enemy('Kenjaku_29.png', 50, 125, 2, 300, 30, 5, 1))

lost = 0
undead = 0
bullets = sprite.Group()
boss = None
boss_active = False

text_win = font2.render("You Win", 1, (0, 0, 255))
text_lose = font2.render('You Lose', 1, (220, 20, 60))
text_boss_defeated = font2.render("Boss Defeated!", 1, (0, 255, 0))
current_weapon_index = 0
last_shot_time = 0
current_weapon = weapons[current_weapon_index]
game = True
finish = True
menu = True

while game:
    if not finish:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    current_weapon = weapons[current_weapon_index]
                    current_time = time.get_ticks()
                    if current_time - last_shot_time >= (1000 / current_weapon.fire_rate):
                        if (current_weapon.name == 'Красный' and player.ammunition_type1 > 0) or \
                           (current_weapon.name == 'Фиолетовый' and player.ammunition_type2 > 0):
                            last_shot_time = current_time
                            player.fire()
                if e.key == K_1:
                    current_weapon_index = 0
                elif e.key == K_2 and len(weapons) > 1:
                    current_weapon_index = 1

        current_weapon = weapons[current_weapon_index]

        window.blit(bg, (0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        buffs.update()
        buffs.draw(window)

        if undead >= 19 and not boss_active:
            monsters.empty()
            boss = Boss('58da6c690f6ef27c00e3aa7495971663.png', 200, 250, 1.5, 250, 0, 5, 80)
            monsters.add(boss)
            boss_active = True

        for buff in sprite.spritecollide(player, buffs, True):
            player.apply_buff()

        monsters_list = sprite.groupcollide(monsters, bullets, False, False)
        for monster in monsters_list:
            for bullet in monsters_list[monster]:
                monster.healthe -= bullet.damage
                if bullet.bullet_type == 1:
                    bullet.kill()
                if monster.healthe <= 0:
                    monster.kill()
                    if not boss_active:
                        undead += 1
                        random_enemy = randint(0, len(enemies_list) - 1)
                        cursed = enemies_list[random_enemy]
                        monsters.add(cursed)
                    else:
                        finish = True
                    if random.random() < 0.2:
                        buffs.add(Buff(monster.rect.x, monster.rect.y, 5000, 'black flash.jpg', 20, 20, 4))

        if boss is not None and boss.healthe <= 0:
            finish = True
            window.blit(text_boss_defeated, (200, 400))

        if boss is not None and boss.rect.colliderect(player.rect):
            finish = True
            window.blit(text_lose, (200, 400))

        if lost >= 23 or player.healthe <= 0:
            finish = True
            window.blit(text_lose, (200, 400))

        clash = sprite.spritecollide(player, monsters, True)
        for monster in clash:
            player.healthe -= monster.damage
            if not boss_active:
                random_enemy = randint(0, len(enemies_list) - 1)
                cursed = enemies_list[random_enemy]
                monsters.add(cursed)

        text_lost = font1.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (20, 20))
        text_score = font1.render("Killed: " + str(undead), 1, (255, 255, 255))
        window.blit(text_score, (20, 50))
        text_healthe = font1.render("Health: " + str(player.healthe), 1, (255, 255, 255))
        window.blit(text_healthe, (20, 80))
        text_ammo1 = font1.render("Красный: " + str(int(player.ammunition_type1)), 1, (255, 255, 255))
        window.blit(text_ammo1, (20, 110))
        text_ammo2 = font1.render("Фиолетовый: " + str(int(player.ammunition_type2)), 1, (255, 255, 255))
        window.blit(text_ammo2, (20, 140))
        if player.rel_time:
            text_reload = font1.render("Reloading...", 1, (255, 255, 0))
            window.blit(text_reload, (20, 170))
        # Display current date and time
        current_time = datetime.now().strftime("%I:%M %p PDT, %A, %B %d, %Y")
        text_datetime = font1.render(current_time, 1, (255, 255, 255))
        window.blit(text_datetime, (800, 200))

    if menu:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if menu_btn.rect.collidepoint(x, y):
                    menu = False
                    finish = False
        window.blit(bg, (0, 0))
        menu_btn.reset()

    if finish and not menu:
        for e in event.get():
            if e.type == QUIT:
                game = False

    clock.tick(60)
    display.update()