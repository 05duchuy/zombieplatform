import pygame
import os
class Item:
    EQUIP_TYPES = ["none", "head", "body", "leg", "foot", "weapon"]

    def __init__(self, item_id, name="Unknown", stack=-1, usable=False, equip_type="none", image=None):
        self.id = f"{int(item_id):02d}"
        self.name = name
        self.stack_max = min(max(stack, -1), 999)
        self.count = 1
        self.usable = bool(usable)
        etype = equip_type.lower()
        self.equip_type = etype if etype in self.EQUIP_TYPES else "none"
        self.image = image

    def is_stackable(self):
        return self.stack_max > 1

def get_predefined_items():
    def load_img(name):
        path = os.path.join("pic", name)
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (40, 40))
        except:
            surf = pygame.Surface((40, 40))
            surf.fill((255, 0, 0))
            return surf

    items = {
        "bandage": Item(
            item_id=1, 
            name="Bandage", 
            stack=20, 
            usable=True, 
            image=load_img("bandage.png")
        ),
        "wood": Item(
            item_id=2, 
            name="Wood", 
            stack=999, 
            usable=False, 
            image=load_img("wood.png")
        ),
        "pistol": Item(
            item_id=3, 
            name="Pistol", 
            stack=-1, 
            equip_type="weapon", 
            image=load_img("pistol.png")
        ),
        "medkit": Item(
            item_id=4, 
            name="Medkit", 
            stack=5, 
            usable=True, 
            image=load_img("medkit.png")
        )
    }
    
    return items