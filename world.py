import pygame
from settings import TILE_SIZE

def draw_textured_platform(surface, rect, tiles):
    for x in range(rect.x, rect.right, TILE_SIZE):
        for y in range(rect.y, rect.bottom, TILE_SIZE):
            tile_pos = (x, y)
            if y == rect.y:
                if x == rect.right - TILE_SIZE:
                    surface.blit(tiles['right_grass'], tile_pos)
                elif x == rect.left:
                    surface.blit(tiles['left_grass'], tile_pos)
                else:
                    surface.blit(tiles['grass'], tile_pos)
            else:
                if x == rect.right - TILE_SIZE:
                    surface.blit(tiles['right_dirt'], tile_pos)
                elif x == rect.left:
                    surface.blit(tiles['left_dirt'], tile_pos)
                else:
                    surface.blit(tiles['dirt'], tile_pos)

def draw_water_platform(surface, rect, tiles):
    for x in range(rect.x, rect.right, TILE_SIZE):
        for y in range(rect.y, rect.bottom, TILE_SIZE):
            tile_pos = (x, y)
            if y == rect.y:
                surface.blit(tiles['water_top'], tile_pos)
            else:
                surface.blit(tiles['water_fill'], tile_pos)