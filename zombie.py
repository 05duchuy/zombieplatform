import pygame
import math
import random
from settings import *
from utils import load_framez

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.max_hp = 100
        self.hp = 100
        self.atk = 15
        self.is_dead = False
        self.death_time = 0

        self.is_attacking = False
        self.attack_start_time = 0
        self.last_attack_time = 0
        self.has_hit_player = False

        self.last_wander_time = 0 
        self.wander_direction = "idle"

        self.animations = {
            "walk": load_framez("Walk", 10, width=90, height=128),
            "idle": load_framez("Idle", 10, width=90, height=128),
            "attack": load_framez("Attack", 10, width=90, height=128),
            "dead": load_framez("Dead", 10, width=140, height=128)
        }
        self.index = 0
        self.image = self.animations["walk"][self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.hitbox = pygame.Rect(0, 0, 50, 90)
        self.hitbox.midbottom = self.rect.midbottom
        
        self.speed = 2
        self.vel_x = 0
        self.vel_y = 0
        self.direction = "right"
        self.on_ground = False

    def check_player_behavior(self, player_hitbox, platforms):
        if self.is_dead: return

        curr_time = pygame.time.get_ticks()
        dist = math.sqrt((self.hitbox.centerx - player_hitbox.centerx)**2 + 
                         (self.hitbox.centery - player_hitbox.centery)**2)

        if dist > 350:
            if curr_time - self.last_wander_time > 3000:
                self.wander_direction = random.choice(["left", "right", "idle"])
                self.last_wander_time = curr_time
            
            if abs(self.vel_x) < self.speed:
                if self.wander_direction == "idle":
                    self.vel_x = 0
                else:
                    self.direction = self.wander_direction
                    self.vel_x = self.speed if self.direction == "right" else -self.speed
                
                if self.on_ground and self.wander_direction != "idle":
                    check_x = self.hitbox.right + 5 if self.direction == "right" else self.hitbox.left - 5
                    check_y = self.hitbox.bottom + 5
                    is_cliff = True
                    for plat in platforms:
                        if plat.collidepoint(check_x, check_y):
                            is_cliff = False
                            break
                    if is_cliff:
                        self.direction = "left" if self.direction == "right" else "right"
                        self.wander_direction = self.direction
                        self.vel_x = self.speed if self.direction == "right" else -self.speed

        else:
            if not self.is_attacking:
                self.direction = "right" if player_hitbox.centerx > self.hitbox.centerx else "left"

            diff_x = abs(self.hitbox.centerx - player_hitbox.centerx)
            
            if dist < 50:
                can_attack = curr_time - self.last_attack_time > ATTACK_COOLDOWN
                
                if can_attack or self.is_attacking:
                    if abs(self.vel_x) < self.speed: self.vel_x = 0
                    
                    if not self.is_attacking and can_attack:
                        self.is_attacking = True
                        self.attack_start_time = curr_time
                        self.index = 0
                        self.has_hit_player = False
                else:
                    if not self.is_attacking and diff_x > 5:
                        self.vel_x = self.speed if self.direction == "right" else -self.speed
            
            elif diff_x < 5:
                if abs(self.vel_x) < self.speed: self.vel_x = 0
            else:
                if not self.is_attacking and abs(self.vel_x) < self.speed:
                    self.vel_x = self.speed if self.direction == "right" else -self.speed

    def take_damage(self, amount):
        if self.is_dead: return
        self.hp -= amount
        self.is_attacking = False
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
            self.death_time = pygame.time.get_ticks()
            self.index = 0

    def apply_knockback(self, direction_factor):
        if self.is_dead: return
        self.vel_x = direction_factor * 6
        self.vel_y = -8
        self.on_ground = False

    def move_and_collide(self, platforms):
        self.hitbox.y += self.vel_y
        self.on_ground = False
        for plat in platforms:
            if self.hitbox.colliderect(plat):
                if self.vel_y > 0:
                    self.hitbox.bottom = plat.top
                    self.vel_y, self.on_ground = 0, True
                elif self.vel_y < 0:
                    self.hitbox.top = plat.bottom
                    self.vel_y = 0

        if not self.is_dead:
            self.hitbox.x += self.vel_x
            for plat in platforms:
                if self.hitbox.colliderect(plat):
                    if self.vel_x > 0: self.hitbox.right = plat.left
                    elif self.vel_x < 0: self.hitbox.left = plat.right
                    self.vel_x = 0

        if self.on_ground:
            self.vel_x *= FRICTION
            if abs(self.vel_x) < 0.1: self.vel_x = 0

        off_x = 10 if self.direction == "right" else -10 
        
        y_offset = 12 if self.is_dead else 3 
        
        if self.is_dead: 
            off_x = 10 if self.direction == "right" else -70
        
        self.rect.midbottom = (self.hitbox.midbottom[0] + off_x, self.hitbox.midbottom[1] + y_offset)

    def is_hitbox_active(self):
        if not self.is_attacking: return False
        elapsed = pygame.time.get_ticks() - self.attack_start_time
        return 200 <= elapsed <= 300

    def get_attack_rect(self):
        att_w = 40
        if self.direction == "right":
            return pygame.Rect(self.hitbox.centerx, self.hitbox.top, att_w + 25, self.hitbox.height)
        return pygame.Rect(self.hitbox.centerx - (att_w + 25), self.hitbox.top, att_w + 25, self.hitbox.height)

    def draw_hp(self, surface):
        if self.is_dead: return
        width, height = 50, 6
        x, y = self.hitbox.centerx - (width // 2), self.hitbox.top - 10
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (128, 128, 128), (x, y, width, height))
        pygame.draw.rect(surface, (255, 0, 0), (x, y, int(width * ratio), height))

    def apply_gravity(self):
        if self.is_dead: return
        self.vel_y += GRAVITY
        if self.vel_y > 15: self.vel_y = 15

    def animate(self):
        if self.is_dead:
            state = "dead"
            self.index += 0.2
            if self.index >= len(self.animations[state]): self.index = len(self.animations[state]) - 1
        elif self.is_attacking:
            state = "attack"
            self.index += 0.83
            if self.index >= len(self.animations[state]): self.index = 0
        else:
            state = "walk" if self.on_ground and abs(self.vel_x) > 0.5 else "idle"
            self.index += 0.2
            if self.index >= len(self.animations[state]): self.index = 0

        self.image = self.animations[state][int(self.index)]
        if self.direction == "left": self.image = pygame.transform.flip(self.image, True, False)

    def update(self, platforms, player_hitbox, water_areas):
        self.apply_gravity()
        self.check_player_behavior(player_hitbox, platforms)
        
        if not self.is_dead:
            for water in water_areas:
                if self.hitbox.colliderect(water):
                    self.take_damage(self.hp)
                    self.vel_y = 0
                    self.vel_x = 0
                    break 

        if self.is_attacking and pygame.time.get_ticks() - self.attack_start_time > 500:
            self.is_attacking = False
            self.last_attack_time = pygame.time.get_ticks()

        self.move_and_collide(platforms)
        self.animate()
        
        if self.is_dead:
            return pygame.time.get_ticks() - self.death_time > 1000
            
        return self.hitbox.left > WIDTH + 100 or self.hitbox.right < -100 or self.hitbox.top > HEIGHT