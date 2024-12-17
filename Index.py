import random
import random

# Define the game entities
class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 15, 10)
        self.inventory = {"water": 2, "vodka": 1}
        self.position = (0, 0)  # Starting position on the map
        self.xp = 0
        self.level = 1
        self.equipment = []  # List to store weapons and armor

    def gain_xp(self, amount):
        self.xp += amount
        print(f"You gained {amount} XP! Total XP: {self.xp}")
        # Check if the player levels up
        xp_needed = self.level * 100
        if self.xp >= xp_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.hp += 20
        self.attack += 5
        self.defense += 3
        print(f"Congratulations! You leveled up to Level {self.level}!")
        print(f"New stats - HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}")

class Monster(Character):
    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)

# Game data
monsters = [
    Monster("Goblin", 30, 10, 5),
    Monster("Troll", 50, 12, 8),
    Monster("Macronus", 9999, 999, 999),
]

# Map data
map_data = {
    (0, 0): "You are at the forest entrance. It's quiet.",
    (1, 0): "You see tall trees surrounding you.",
    (2, 0): "A clearing with some strange markings on the ground.",
    (3, 0): "The boss Macronus awaits here!",
    (0, 1): "A small stream flows gently.",
    (1, 1): "You found a broken sword on the ground.",
    (2, 1): "Dense fog makes it hard to see.",
    (3, 1): "The trees open up to a vast clearing.",
}

# Directions
valid_directions = {"north", "south", "east", "west"}

directions = {
    "north": (0, 1),
    "south": (0, -1),
    "east": (1, 0),
    "west": (-1, 0),
}

# Items that can be found
consumables = ["water", "vodka"]
weapons = ["Iron Sword", "Steel Axe", "Magic Wand"]
armor = ["Leather Armor", "Chainmail"]

# Get available directions for the current position
def get_available_directions(player):
    available_directions = []
    for direction, (dx, dy) in directions.items():
        new_position = (player.position[0] + dx, player.position[1] + dy)
        if new_position in map_data:
            available_directions.append(direction)
    return available_directions

def check_for_item(player):
    chance = random.random()
    if chance < 0.3:  # 30% chance to find a consumable
        item = random.choice(consumables)
        player.inventory[item] = player.inventory.get(item, 0) + 1
        print(f"You found a {item}! It has been added to your inventory.")
    elif chance < 0.5:  # 20% chance to find a weapon
        weapon = random.choice(weapons)
        player.equipment.append(weapon)
        player.attack += 5  # Increase attack with a weapon
        print(f"You found a {weapon}! Your attack increases by 5.")
    elif chance < 0.6:  # 10% chance to find armor
        piece = random.choice(armor)
        player.equipment.append(piece)
        player.defense += 3  # Increase defense with armor
        print(f"You found {piece}! Your defense increases by 3.")

# Combat system
def combat(player, monster):
    print(f"You encountered {monster.name}!")

    while player.hp > 0 and monster.hp > 0:
        print(f"\n{player.name}'s HP: {player.hp} | {monster.name}'s HP: {monster.hp}")
        print("1. Attack with Nose Breaker")
        print("2. Attack with Family Balls Breaker")
        print("3. Use item")
        print("4. Run")
        choice = input("What do you do? ").strip()

        if choice == "1":
            damage = max(player.attack - monster.defense, 1)
            monster.hp -= damage
            print(f"You hit {monster.name} with Nose Breaker for {damage} damage!")
        elif choice == "2":
            damage = max((player.attack + 5) - monster.defense, 1)
            monster.hp -= damage
            print(f"You hit {monster.name} with Family Balls Breaker for {damage} damage!")
        elif choice == "3":
            use_item(player)
        elif choice == "4":
            print("You ran away!")
            return False
        else:
            print("Invalid choice! Please try again.")
            continue

        if monster.hp > 0:
            monster_damage = max(monster.attack - player.defense, 1)
            player.hp -= monster_damage
            print(f"{monster.name} hits you for {monster_damage} damage!")

    if player.hp > 0:
        print(f"You defeated {monster.name}!")
        xp_gain = 50  # XP reward for defeating the monster
        player.gain_xp(xp_gain)
        return True
    else:
        print("You were defeated...")
        return False

# Use items
def use_item(player):
    print("Inventory:")
    for item, count in player.inventory.items():
        print(f"{item.capitalize()}: {count}")

    choice = input("Which item do you want to use? ").strip().lower()
    if choice in player.inventory and player.inventory[choice] > 0:
        if choice == "water":
            player.hp += 20
            print("You used water and restored 20 HP!")
        elif choice == "vodka":
            player.hp += 50
            print("You used vodka and restored 50 HP!")
        player.inventory[choice] -= 1
    else:
        print("Invalid item or out of stock!")

# Main game loop
def move_player(player, direction):
    dx, dy = directions.get(direction.lower(), (0, 0))
    new_position = (player.position[0] + dx, player.position[1] + dy)

    if new_position in map_data:
        player.position = new_position
        print(map_data[new_position])
        check_for_item(player)
        return True
    else:
        print("You cannot go that way!")
        return False

def main():
    print("Welcome to the RPG Game!")
    print("Rules:")
    print("1. Navigate the forest using directions: north, south, east, or west.")
    print("2. Fight monsters using your attacks or items.")
    print("3. Gain XP to level up and become stronger.")
    print("4. Collect items like water, vodka, weapons, and armor to improve your stats.")
    print("5. Defeat the boss Macronus to win the game.")
    print("6. Beware, Macronus is extremely powerful!")

    name = input("Enter your character's name: ").strip()
    player = Player(name)

    print("\nYour journey begins in a mysterious forest...")

    while player.hp > 0:
        available_directions = get_available_directions(player)
        print(f"\nAvailable directions: {', '.join(direction.capitalize() for direction in available_directions)}")
        direction = input("Which direction do you want to go? ").strip().lower()

        if direction in available_directions:
            moved  = move_player(player, direction)
            if not moved:
                continue

            if player.position == (3, 0):  # Boss position
                print("You encounter Macronus!")
                if not combat(player, monsters[-1]):  # If combat ends with player defeat
                    break
                else:
                    print("You defeated the boss and won the game!")
                    break

            # Random encounters
            if random.random() < 0.5:  # 50% chance of encountering a monster
                monster = random.choice(monsters[:-1])  # Exclude the boss
                if not combat(player, monster):  # Engage in combat
                    break  # End the game loop if player is defeated
        else:
            print("Invalid direction! Please choose from the available directions.")

    print("Game Over")  # End of the game after player defeat or victory

if __name__ == "__main__":
    main()
