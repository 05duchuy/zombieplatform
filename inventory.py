import copy
import os

class Inventory:
    MAX_SLOTS = 30

    def __init__(self):
        self.slots = [None] * self.MAX_SLOTS

    def add_item(self, item_template, amount):
        if amount <= 0: return
        
        if item_template.is_stackable():
            for slot in self.slots:
                if slot and slot.id == item_template.id and slot.count < 999:
                    add_amount = min(amount, 999 - slot.count)
                    slot.count += add_amount
                    amount -= add_amount
                    if amount <= 0: break

        while amount > 0:
            try:
                empty_idx = self.slots.index(None)
                new_item = copy.copy(item_template)
                if not item_template.is_stackable():
                    new_item.count = 1
                    self.slots[empty_idx] = new_item
                    amount -= 1
                else:
                    new_item.count = min(amount, 999)
                    self.slots[empty_idx] = new_item
                    amount -= new_item.count
                if all(s is not None for s in self.slots): break
            except ValueError: break

    def save_to_file(self, filename="savegame.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for slot in self.slots:
                if slot:
                    f.write(f"{slot.id} {slot.count}\n")

    def load_from_file(self, filename, item_db):
        if not os.path.exists(filename): return
        self.slots = [None] * self.MAX_SLOTS
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    i_id, i_count = parts
                    template = next((v for v in item_db.values() if v.id == i_id), None)
                    if template:
                        self.add_item(template, int(i_count))