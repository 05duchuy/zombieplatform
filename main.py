import pygame
import os
import random
from settings import *
from utils import load_tile
from world import draw_textured_platform, draw_water_platform
from player import Player
from zombie import Zombie
from menu import Menu
from item import get_predefined_items
from inventory import Inventory

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")
clock = pygame.time.Clock()

bg_surface = pygame.image.load(os.path.join("pic/map", "BG.png")).convert()
bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))

item_db = get_predefined_items()

tiles = {
    'grass': load_tile("2"), 'dirt': load_tile("5"),
    'left_grass': load_tile("1"), 'right_grass': load_tile("3"),
    'left_dirt': load_tile("4"), 'right_dirt': load_tile("6"),
    'water_top': load_tile("17"), 'water_fill': load_tile("18")
}

tree_img = pygame.image.load(os.path.join("pic/map", "Tree.png")).convert_alpha()
tree_img = pygame.transform.scale(tree_img, (150, 200))
trees_list = [(600, 50), (100, 0), (650, 400), (1050,-50)]

bush_img = pygame.image.load(os.path.join("pic/map", "Bush.png")).convert_alpha()
bush_img = pygame.transform.scale(bush_img, (75, 50))
bushes_list = [(900, 350), (460, 250), (250, 400)]

mushroom_img = pygame.image.load(os.path.join("pic/map", "Mushroom.png")).convert_alpha()
mushroom_img = pygame.transform.scale(mushroom_img, (25, 20))
mushrooms_list = [(130, 180), (750, 580), (620, 230)]

stone_img = pygame.image.load(os.path.join("pic/map", "Stone.png")).convert_alpha()
stone_img = pygame.transform.scale(stone_img, (75, 50))
stones_list = [(950, 100), (500, 550)]

player = Player()
game_menu = Menu()
player_inv = Inventory()
zombies = []
last_spawn_time = pygame.time.get_ticks()  

level_platforms = [
    pygame.Rect(50, 200, 200, 50), pygame.Rect(900, 150, 300, 50),
    pygame.Rect(450, 300, 150, 50), pygame.Rect(600, 250, 150, 100),
    pygame.Rect(50, 600, 1050, 250), pygame.Rect(850, 400, 150, 50),
    pygame.Rect(1150, 300, 150, 50), pygame.Rect(150, 450, 200, 50)
]
water_areas = [pygame.Rect(1050, 600, 550, 250), pygame.Rect(-250, 600, 700, 250)]
player_inv.load_from_file("savegame.txt", item_db)

# --- Main loops ---
running = True
while running:
    curr_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                result = game_menu.handle_click(pygame.mouse.get_pos(), player_inv)
                if result == "quit":
                    running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                game_menu.toggle(player_inv)

            if not game_menu.is_active:
                if event.key == pygame.K_k:
                    player.toggle_aura()

    if not game_menu.is_active:
        player.update(level_platforms, water_areas) #

        if player.hp > 0:
            if len(zombies) < 10 and curr_time - last_spawn_time > ZOMBIE_SPAWN_TIME:
                random_tree = random.choice(trees_list)
                zombies.append(Zombie(random_tree[0] + 50, random_tree[1] + 50))
                last_spawn_time = curr_time

            if player.is_hitbox_active():
                attack_rect = player.get_attack_rect()
                for z in zombies:
                    if attack_rect.colliderect(z.hitbox) and z not in player.hit_zombies:
                        z.take_damage(player.atk)
                        z_kb_dir = 1 if player.hitbox.centerx < z.hitbox.centerx else -1
                        z.apply_knockback(z_kb_dir)
                        player.hit_zombies.append(z)

            for z in zombies[:]:
                if z.update(level_platforms, player.hitbox, water_areas):
                    zombies.remove(z)
                    continue
                
                if z.is_hitbox_active():
                    z_rect = z.get_attack_rect()
                    if z_rect.colliderect(player.hitbox) and not z.has_hit_player:
                        player.hp -= z.atk
                        p_kb_dir = 1 if z.hitbox.centerx < player.hitbox.centerx else -1
                        if hasattr(player, 'apply_knockback'):
                            player.apply_knockback(p_kb_dir)
                        z.has_hit_player = True
        else:
            zombies.clear()

    screen.blit(bg_surface, (0, 0))

    for w in water_areas: draw_water_platform(screen, w, tiles)
    for pos in trees_list: screen.blit(tree_img, pos)
    for pos in mushrooms_list: screen.blit(mushroom_img, pos)
    for pos in stones_list: screen.blit(stone_img, pos)
    for p in level_platforms: draw_textured_platform(screen, p, tiles)

    if not player.is_dead and player.aura_active:
        screen.blit(player.aura.image, player.aura.rect)
    
    for z in zombies:
        screen.blit(z.image, z.rect)
        z.draw_hp(screen)
    screen.blit(player.image, player.rect)
    
    for pos in bushes_list: screen.blit(bush_img, pos)
        
    player.draw_hp(screen)
    
    game_menu.draw(screen, player, player_inv) 

    if DEBUG_MODE:
        pygame.draw.rect(screen, (0, 255, 0), player.hitbox, 2)
        for z in zombies:
            pygame.draw.rect(screen, (255, 0, 0), z.hitbox, 2)
        if player.is_hitbox_active():
            pygame.draw.rect(screen, (255, 255, 0), player.get_attack_rect(), 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()