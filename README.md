# zombieplatform
zombieplatform
# Overview
Zombie Survival is a 2D action-platformer designed to explore complex game systems, including advanced AI behaviors, frame-based combat mechanics, and a robust inventory management system. This project serves as a deep dive into "Action-System Design," focusing on how various mechanics interact to create a challenging and persistent gameplay experience.

# Controls
W, A, D: Move and Jump.

J: Basic Attack.

K: Activate Aura (Power-up).

E or ESC: Toggle Inventory Menu.

Mouse: Drag and drop items; interact with menu buttons.

# Gameplay Mechanics
Combat System: Uses a frame-based hitbox logic where attacks are only active during specific animation frames (200ms–300ms). This requires players to time their strikes precisely rather than simply spamming buttons.

Knockback Logic: Both the player and enemies experience directional knockback upon taking damage, creating tactical spacing during combat.

Aura System: A "Risk vs. Reward" mechanic that grants temporary buffs (+50 Attack and 1.5x Speed) but is governed by a strict duration and cooldown timer.

Environmental Hazards: Includes water platforms that result in instant character death, adding a layer of platforming risk.

# AI Design
The project features a Finite State Machine (FSM) for zombie behavior to simulate realistic threats:

Wander State: AI moves randomly and includes "Cliff Detection" to prevent walking off edges.

Chase State: Triggered when the player is within a 350px radius, prompting the AI to navigate toward the player's position.

Attack State: AI evaluates distance to determine when to stop moving and initiate a strike animation.

# Inventory and Persistence
Grid-Based Inventory: A 30-slot system supporting item categorization (Usable vs. Equipment) and stackable logic for up to 999 items.

Drag and Drop: Players can manually organize their inventory by moving items between slots.

Data Persistence: Player stats and inventory contents are saved to and loaded from a local "savegame.txt" file to ensure long-term retention.

# Technical Stack
Language: Python.

Library: Pygame.

Core Concepts: State Management, Physics-based movement (Gravity/Friction), and Vector Math for AI tracking.