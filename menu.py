import pygame
import os
from settings import WIDTH, HEIGHT

class Menu:
    def __init__(self):

        self.save_rect = pygame.Rect(0, 0, 100, 40)
        self.save_quit_rect = pygame.Rect(0, 0, 100, 40)
        self.quit_rect = pygame.Rect(0, 0, 100, 40)

        self.is_active = False
        pygame.font.init()
        self.font = pygame.font.SysFont("Tahoma", 20, bold=True)
        
        self.carried_item = None
        self.original_idx = -1
        self.idle_index = 0

        self.start_x = 462  
        self.start_y = 64   
        self.gap_x = 55     
        self.gap_y = 53     
        self.slot_size = 40 

        try:
            self.image = pygame.image.load(os.path.join("pic", "menugame.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (1000, 400))
            self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        except:
            self.image = pygame.Surface((1000, 400))
            self.image.fill((50, 50, 50))
            self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def toggle(self, inventory):
        self.is_active = not self.is_active
        if not self.is_active and self.carried_item:
            inventory.slots[self.original_idx] = self.carried_item
            self.carried_item = None
            self.original_idx = -1

    def handle_click(self, mouse_pos, inventory):
        if not self.is_active: return
        mx, my = mouse_pos

        if self.save_rect.collidepoint(mx, my):
            inventory.save_to_file("savegame.txt")
            return "save"
        if self.save_quit_rect.collidepoint(mx, my):
            inventory.save_to_file("savegame.txt")
            return "quit"
        if self.quit_rect.collidepoint(mx, my):
            return "quit"

        for i in range(30):
            col = i % 10
            row = i // 10
            slot_x = self.rect.x + self.start_x + col * self.gap_x
            slot_y = self.rect.y + self.start_y + row * self.gap_y
            
            slot_rect = pygame.Rect(slot_x - self.slot_size//2, slot_y - self.slot_size//2, self.slot_size, self.slot_size)

            if slot_rect.collidepoint(mx, my):
                if self.carried_item is None:
                    if inventory.slots[i] is not None:
                        self.carried_item = inventory.slots[i]
                        inventory.slots[i] = None
                        self.original_idx = i
                else:
                    temp = inventory.slots[i]
                    inventory.slots[i] = self.carried_item
                    self.carried_item = temp
                    if self.carried_item is None:
                        self.original_idx = -1
                break
        return "continue"

    def draw(self, screen, player, inventory):
        if not self.is_active: return

        self.save_rect.topleft = (self.rect.x + 659, self.rect.y + 275)
        self.save_quit_rect.topleft = (self.rect.x + 769, self.rect.y + 275)
        self.quit_rect.topleft = (self.rect.x + 879, self.rect.y + 275)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        screen.blit(overlay, (0, 0))
        
        screen.blit(self.image, self.rect)

        self.idle_index += 0.3
        idle_frames = player.animations["idle"]
        char_img = idle_frames[int(self.idle_index) % len(idle_frames)]
        screen.blit(char_img, (self.rect.x + 165, self.rect.y + 110))

        hp_text = f"HP: {int(player.hp)} / {int(player.max_hp)}"
        screen.blit(self.font.render(hp_text, True, (255, 255, 255)), (self.rect.x + 130, self.rect.y + 260))

        atk_text = f"ATK: {int(player.atk)}"
        screen.blit(self.font.render(atk_text, True, (255, 255, 255)), (self.rect.x + 130, self.rect.y + 285))

        spd_text = f"SPD: {int(player.current_max_speed)}"
        screen.blit(self.font.render(spd_text, True, (255, 255, 255)), (self.rect.x + 130, self.rect.y + 310))

        count_font = pygame.font.SysFont("Tahoma", 14, bold=True)
        for i, item in enumerate(inventory.slots):
            if item is None: continue 
            
            col = i % 10
            row = i // 10
            item_x = self.rect.x + self.start_x + col * self.gap_x
            item_y = self.rect.y + self.start_y + row * self.gap_y
            
            img_rect = item.image.get_rect(center=(item_x, item_y))
            screen.blit(item.image, img_rect)
            
            if item.count > 1:
                count_surf = count_font.render(str(item.count), True, (255, 255, 255))
                screen.blit(count_surf, (item_x + 5, item_y + 5))

        if self.carried_item:
            mx, my = pygame.mouse.get_pos()
            img_rect = self.carried_item.image.get_rect(center=(mx, my))
            screen.blit(self.carried_item.image, img_rect)
            if self.carried_item.count > 1:
                count_surf = count_font.render(str(self.carried_item.count), True, (255, 255, 255))
                screen.blit(count_surf, (mx + 5, my + 5))

        save_surf = self.font.render("SAVE", True, (255, 255, 255))
        sq_surf = self.font.render("S & Q", True, (255, 255, 255))
        quit_surf = self.font.render("QUIT", True, (255, 255, 255))

        screen.blit(save_surf, save_surf.get_rect(center=self.save_rect.center))
        screen.blit(sq_surf, sq_surf.get_rect(center=self.save_quit_rect.center))
        screen.blit(quit_surf, quit_surf.get_rect(center=self.quit_rect.center))

        pygame.draw.rect(screen, (255, 0, 0), self.save_rect, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.save_quit_rect, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.quit_rect, 2)