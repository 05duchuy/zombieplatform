import pygame
import os
from settings import TILE_SIZE

def load_tile(name):
    path = os.path.join("pic/map", f"{name}.png")
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    else:
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surf.fill((100, 100, 100))
        return surf

def load_frames(action, count, width=90, height=128):
    frames = []
    for i in range(1, count + 1):
        path = os.path.join("pic/charac", f"{action} ({i}).png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            frames.append(img)
        else:
            surf = pygame.Surface((width, height))
            surf.fill((200, 0, 200))
            frames.append(surf)
    return frames

def load_framez(action, count, width=90, height=128):
    frames = []
    for i in range(1, count + 1):
        path = os.path.join("pic/zombie", f"{action} ({i}).png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            frames.append(img)
        else:
            surf = pygame.Surface((width, height))
            surf.fill((200, 0, 200))
            frames.append(surf)
    return frames

def load_aura_frames(folder, count, width=150, height=150):
    frames = []
    for i in range(1, count + 1):
        filename = f"{str(i).zfill(5)}.png"
        path = os.path.join("pic", folder, filename)
        
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            frames.append(img)
        else:
            print(f"Warning: Thiếu file {path}")
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            frames.append(surf)
    return frames
