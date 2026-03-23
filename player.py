import pygame
import os
from settings import *
from utils import load_frames
from utils import load_aura_frames

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_hp = PLAYER_HP
        self.hp = PLAYER_HP
        
        self.base_atk = PLAYER_ATK
        self.atk = PLAYER_ATK
        self.base_max_speed = MAX_SPEED
        self.current_max_speed = MAX_SPEED

        self.aura_active = False
        self.aura_timer = 0
        self.aura_cd_timer = 0
        self.max_aura_time = 120
        self.max_aura_cd = 360

        self.is_dead = False
        self.death_time = 0

        self.animations = {
            "idle": load_frames("Idle", 10),
            "walk": load_frames("Run", 10),
            "jump": load_frames("Jump", 10),
            "attack": load_frames("Attack", 10),
            "jump_attack": load_frames("JumpAttack", 10),
            "dead": load_frames("Dead", 10, width=130, height=128)
        }
        self.start_x, self.start_y = 200, 300
        self.aura = Aura(self) 
        self.index = 0
        self.image = self.animations["idle"][self.index]
        self.rect = self.image.get_rect(center=(self.start_x, self.start_y))
        self.hitbox = pygame.Rect(0, 0, 50, 90)
        self.hitbox.midbottom = self.rect.midbottom
        self.vel_x, self.vel_y = 0, 0
        self.is_attacking = False
        self.attack_start_time = 0
        self.hit_zombies = []
        self.last_attack_time = 0
        self.direction = "right"
        self.on_ground = False
        self.is_moving = False

        try:
            self.sound_walk = pygame.mixer.Sound(os.path.join("sound", "walk.wav"))
            self.sound_jump = pygame.mixer.Sound(os.path.join("sound", "jump.wav"))
            self.sound_attack = pygame.mixer.Sound(os.path.join("sound", "attack.wav"))
            self.walk_channel = pygame.mixer.Channel(0)
        except:
            self.sound_walk = self.sound_jump = self.sound_attack = None
            self.walk_channel = None

    def handle_input(self):
        if self.is_dead: return
        keys = pygame.key.get_pressed()
        curr_time = pygame.time.get_ticks()

        if not self.is_attacking:
            if keys[pygame.K_w] and self.on_ground:
                self.vel_y = JUMP_POWER
                self.on_ground = False
                if self.sound_jump:
                    chan = pygame.mixer.find_channel(True)
                    if chan: chan.play(self.sound_jump)
            
            if keys[pygame.K_a]:
                self.vel_x -= ACCELERATION
                self.direction = "left"
                self.is_moving = True
            elif keys[pygame.K_d]:
                self.vel_x += ACCELERATION
                self.direction = "right"
                self.is_moving = True
            else:
                self.is_moving = False
        
        if keys[pygame.K_j] and not self.is_attacking:
            if curr_time - self.last_attack_time > ATTACK_COOLDOWN:
                self.is_attacking = True
                self.attack_start_time = curr_time
                self.index = 0
                self.hit_zombies = []
                if self.sound_attack:
                    chan = pygame.mixer.find_channel(True)
                    if chan: chan.play(self.sound_attack)

        self.vel_x = max(-MAX_SPEED, min(self.vel_x, MAX_SPEED))

    def update(self, platforms, water_tiles):
        if self.aura_active:
            self.aura_timer -= 1
            if self.aura_timer <= 0:
                self.aura_active = False
                self.atk = self.base_atk
                self.current_max_speed = self.base_max_speed
            else:
                self.aura.update()

        if self.aura_cd_timer > 0:
            self.aura_cd_timer -= 1

        if not self.is_dead:
            self.handle_input()
            self.apply_gravity()
            self.move_and_collide(platforms)
            
            for water in water_tiles:
                if self.hitbox.colliderect(water):
                    self.hp = 0
                    break
            
            if self.hp <= 0:
                self.is_dead = True
                self.death_time = pygame.time.get_ticks()
                self.vel_x = self.vel_y = self.index = 0
                self.aura_active = False
                self.atk = self.base_atk
                self.current_max_speed = self.base_max_speed
        else:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.death_time > RESPAWN_TIME:
                self.is_dead = False
                self.hp = self.max_hp
                self.hitbox.center = (self.start_x, self.start_y + 45)
                self.vel_x = self.vel_y = 0
        
        if self.is_attacking:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.attack_start_time > 500:
                self.is_attacking = False
                self.last_attack_time = curr_time

        self.vel_x = max(-self.current_max_speed, min(self.vel_x, self.current_max_speed))
        self.animate()
        self.update_sprite_position()

    def is_hitbox_active(self):
        if not self.is_attacking: return False
        elapsed = pygame.time.get_ticks() - self.attack_start_time
        return 200 <= elapsed <= 300

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > 15: self.vel_y = 15

    def move_and_collide(self, platforms):
        self.hitbox.x += self.vel_x
        for plat in platforms:
            if self.hitbox.colliderect(plat):
                if self.vel_x > 0: self.hitbox.right = plat.left
                if self.vel_x < 0: self.hitbox.left = plat.right
                self.vel_x = 0

        self.on_ground = False
        self.hitbox.y += self.vel_y
        for plat in platforms:
            if self.hitbox.colliderect(plat):
                if self.vel_y > 0:
                    self.hitbox.bottom = plat.top
                    self.vel_y, self.on_ground = 0, True
                elif self.vel_y < 0:
                    self.hitbox.top = plat.bottom
                    self.vel_y = 0
        self.vel_x *= FRICTION

    def update_sprite_position(self):
        off_x = 10 if self.direction == "right" else -10
        if self.is_dead: off_x = -40 if self.direction == "right" else 0
        self.rect.midbottom = (self.hitbox.midbottom[0] + off_x, self.hitbox.midbottom[1] + 9)

    def animate(self):
        anim_speed = 0.83 if self.is_attacking else 0.6
        self.index += anim_speed
        
        if self.is_dead: state = "dead"
        elif self.is_attacking: state = "attack" if self.on_ground else "jump_attack"
        elif not self.on_ground: state = "jump"
        elif self.is_moving and abs(self.vel_x) > 0.5: state = "walk"
        else: state = "idle"

        if self.index >= len(self.animations[state]):
            self.index = (len(self.animations[state]) - 1) if self.is_dead else 0
        self.image = self.animations[state][int(self.index)]
        if self.direction == "left": self.image = pygame.transform.flip(self.image, True, False)

    def get_attack_rect(self):
        att_w = 30
        if self.direction == "right":
            return pygame.Rect(self.hitbox.right, self.hitbox.top, att_w, self.hitbox.height)
        return pygame.Rect(self.hitbox.left - att_w, self.hitbox.top, att_w, self.hitbox.height)

    def draw_hp(self, surface):
        x, y = self.hitbox.centerx - 25, self.hitbox.top - 10
        width, height = 50, 6
        
        pygame.draw.rect(surface, (128, 128, 128), (x, y, width, height))
        if self.hp > 0:
            pygame.draw.rect(surface, (0, 0, 153), (x, y, int(width * (self.hp/self.max_hp)), height))

        cd_y = y - 10
        if self.aura_active:
            ratio = self.aura_timer / self.max_aura_time
            pygame.draw.rect(surface, (200, 200, 0), (x, cd_y, int(width * ratio), height))
        elif self.aura_cd_timer > 0:
            ratio_cd = 1 - (self.aura_cd_timer / self.max_aura_cd)
            pygame.draw.rect(surface, (50, 50, 50), (x, cd_y, width, height))
            pygame.draw.rect(surface, (0, 200, 0), (x, cd_y, int(width * ratio_cd), height))

    def apply_knockback(self, direction_factor):
        self.vel_x = direction_factor * 12 
        self.vel_y = -8
        self.on_ground = False

    def toggle_aura(self):
        if self.is_dead: return
        
        if not self.aura_active and self.aura_cd_timer <= 0:
            self.aura_active = True
            self.aura_timer = self.max_aura_time
            self.aura_cd_timer = self.max_aura_cd
            
            self.atk = self.base_atk + 50
            self.current_max_speed = self.base_max_speed * 1.5

class Aura(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner  
        self.frames = load_aura_frames("aura", 9, width=180, height=180) 
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        self.index += 0.5
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]
        self.rect.centerx = self.owner.hitbox.centerx
        self.rect.centery = self.owner.hitbox.centery - 30