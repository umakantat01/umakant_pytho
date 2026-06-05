"""
Main Game Module - Multi-character game with lobby, dresses, and weapons
"""
import random
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum
import json


class GunType(Enum):
    """20 Different Gun Types"""
    PISTOL = {"name": "Pistol", "damage": 15, "ammo": 30}
    REVOLVER = {"name": "Revolver", "damage": 25, "ammo": 6}
    RIFLE = {"name": "Rifle", "damage": 50, "ammo": 20}
    SNIPER = {"name": "Sniper Rifle", "damage": 100, "ammo": 5}
    SHOTGUN = {"name": "Shotgun", "damage": 60, "ammo": 8}
    SMG = {"name": "Submachine Gun", "damage": 20, "ammo": 50}
    ASSAULT_RIFLE = {"name": "Assault Rifle", "damage": 45, "ammo": 30}
    LMG = {"name": "Light Machine Gun", "damage": 35, "ammo": 200}
    LASER_RIFLE = {"name": "Laser Rifle", "damage": 55, "ammo": 40}
    PLASMA_GUN = {"name": "Plasma Gun", "damage": 70, "ammo": 20}
    MINIGUN = {"name": "Minigun", "damage": 40, "ammo": 500}
    FLAMETHROWER = {"name": "Flamethrower", "damage": 65, "ammo": 100}
    ROCKET_LAUNCHER = {"name": "Rocket Launcher", "damage": 150, "ammo": 6}
    GRENADE_LAUNCHER = {"name": "Grenade Launcher", "damage": 80, "ammo": 12}
    BEAM_CANNON = {"name": "Beam Cannon", "damage": 120, "ammo": 15}
    PULSE_RIFLE = {"name": "Pulse Rifle", "damage": 48, "ammo": 25}
    RAIL_GUN = {"name": "Rail Gun", "damage": 110, "ammo": 8}
    CROSSBOW = {"name": "Crossbow", "damage": 35, "ammo": 20}
    ENERGY_BLASTER = {"name": "Energy Blaster", "damage": 75, "ammo": 30}
    CYBER_PISTOL = {"name": "Cyber Pistol", "damage": 22, "ammo": 40}


class Dress:
    """Character Dress/Skin"""
    def __init__(self, name: str, rarity: str, bonus: Dict):
        self.name = name
        self.rarity = rarity  # common, rare, epic, legendary
        self.bonus = bonus  # e.g., {"defense": 5, "speed": 2}

    def __repr__(self):
        return f"{self.name} ({self.rarity})"


class Character:
    """Game Character"""
    def __init__(self, char_id: int, name: str, character_class: str):
        self.char_id = char_id
        self.name = name
        self.character_class = character_class
        self.health = 100
        self.armor = 0
        self.speed = 10
        self.dresses: List[Dress] = []
        self.current_dress = None
        self.weapons: List[Dict] = []
        self.current_weapon = None
        self.level = 1
        self.experience = 0

    def equip_dress(self, dress: Dress):
        """Equip a dress/skin"""
        if dress in self.dresses:
            self.current_dress = dress
            self.armor += dress.bonus.get("defense", 0)
            self.speed += dress.bonus.get("speed", 0)
            return True
        return False

    def add_dress(self, dress: Dress):
        """Add dress to inventory"""
        self.dresses.append(dress)

    def equip_weapon(self, gun_name: str):
        """Equip a weapon"""
        for weapon in self.weapons:
            if weapon["name"] == gun_name:
                self.current_weapon = weapon
                return True
        return False

    def add_weapon(self, gun_enum: GunType):
        """Add weapon to inventory"""
        gun_data = gun_enum.value
        weapon = {
            "name": gun_data["name"],
            "damage": gun_data["damage"],
            "ammo": gun_data["ammo"],
            "current_ammo": gun_data["ammo"]
        }
        self.weapons.append(weapon)

    def take_damage(self, damage: int):
        """Take damage with armor reduction"""
        reduced_damage = max(1, damage - self.armor // 2)
        self.health -= reduced_damage
        return self.health

    def __repr__(self):
        return f"Character: {self.name} ({self.character_class}) - Level {self.level}"


class GameLobby:
    """Game Lobby System"""
    def __init__(self, lobby_id: int, max_players: int = 4):
        self.lobby_id = lobby_id
        self.max_players = max_players
        self.players: List[Character] = []
        self.status = "waiting"  # waiting, ready, in_game, completed
        self.created_at = None
        self.game_mode = "deathmatch"  # deathmatch, team, survival

    def add_player(self, character: Character) -> bool:
        """Add player to lobby"""
        if len(self.players) < self.max_players:
            self.players.append(character)
            return True
        return False

    def remove_player(self, character: Character) -> bool:
        """Remove player from lobby"""
        if character in self.players:
            self.players.remove(character)
            return True
        return False

    def is_full(self) -> bool:
        """Check if lobby is full"""
        return len(self.players) >= self.max_players

    def is_ready(self) -> bool:
        """Check if all players are ready"""
        return len(self.players) > 0 and all(
            p.current_weapon is not None for p in self.players
        )

    def start_game(self) -> bool:
        """Start the game"""
        if self.is_ready():
            self.status = "in_game"
            return True
        return False

    def __repr__(self):
        return f"Lobby {self.lobby_id}: {len(self.players)}/{self.max_players} players [{self.status}]"


class CharacterFactory:
    """Factory to create different character types"""
    
    CHARACTER_TYPES = {
        "Warrior": {"health": 120, "armor": 15, "speed": 8},
        "Archer": {"health": 80, "armor": 5, "speed": 14},
        "Mage": {"health": 70, "armor": 0, "speed": 12},
        "Assassin": {"health": 75, "armor": 8, "speed": 16},
        "Knight": {"health": 130, "armor": 25, "speed": 6},
        "Ranger": {"health": 85, "armor": 10, "speed": 13},
        "Paladin": {"health": 110, "armor": 20, "speed": 8},
        "Rogue": {"health": 65, "armor": 5, "speed": 18},
    }

    @staticmethod
    def create_character(char_id: int, name: str, character_class: str) -> Character:
        """Create a character with class-specific attributes"""
        if character_class not in CharacterFactory.CHARACTER_TYPES:
            character_class = "Warrior"
        
        char = Character(char_id, name, character_class)
        attrs = CharacterFactory.CHARACTER_TYPES[character_class]
        char.health = attrs["health"]
        char.armor = attrs["armor"]
        char.speed = attrs["speed"]
        return char


class GameManager:
    """Main Game Manager"""
    def __init__(self):
        self.lobbies: Dict[int, GameLobby] = {}
        self.characters: Dict[int, Character] = {}
        self.dresses: List[Dress] = self._initialize_dresses()
        self.lobby_counter = 0
        self.char_counter = 0

    def _initialize_dresses(self) -> List[Dress]:
        """Initialize available dresses"""
        dresses = [
            # Common Dresses
            Dress("Classic Outfit", "common", {"defense": 0, "speed": 0}),
            Dress("Casual Wear", "common", {"defense": 1, "speed": 1}),
            Dress("Training Gear", "common", {"defense": 2, "speed": 0}),
            Dress("Scout Uniform", "common", {"defense": 0, "speed": 3}),
            # Rare Dresses
            Dress("Combat Armor", "rare", {"defense": 5, "speed": -1}),
            Dress("Leather Jacket", "rare", {"defense": 3, "speed": 2}),
            Dress("Tactical Suit", "rare", {"defense": 4, "speed": 1}),
            Dress("Stealth Gear", "rare", {"defense": 2, "speed": 4}),
            # Epic Dresses
            Dress("Dragon Slayer Armor", "epic", {"defense": 8, "speed": 0}),
            Dress("Shadow Cloak", "epic", {"defense": 4, "speed": 6}),
            Dress("Enchanted Robes", "epic", {"defense": 6, "speed": 3}),
            Dress("Mystic Armor", "epic", {"defense": 7, "speed": 2}),
            # Legendary Dresses
            Dress("Legendary Plate", "legendary", {"defense": 12, "speed": -2}),
            Dress("Dark Phantom Suit", "legendary", {"defense": 10, "speed": 8}),
            Dress("Celestial Armor", "legendary", {"defense": 10, "speed": 5}),
            Dress("Void Walker Cloak", "legendary", {"defense": 8, "speed": 10}),
        ]
        return dresses

    def create_lobby(self, max_players: int = 4) -> GameLobby:
        """Create a new lobby"""
        self.lobby_counter += 1
        lobby = GameLobby(self.lobby_counter, max_players)
        self.lobbies[self.lobby_counter] = lobby
        return lobby

    def create_character(self, name: str, character_class: str) -> Character:
        """Create a new character"""
        self.char_counter += 1
        char = CharacterFactory.create_character(self.char_counter, name, character_class)
        self.characters[self.char_counter] = char
        return char

    def get_all_guns(self) -> List[Dict]:
        """Get all available guns"""
        guns = []
        for gun in GunType:
            gun_data = gun.value
            guns.append({
                "name": gun_data["name"],
                "damage": gun_data["damage"],
                "ammo": gun_data["ammo"]
            })
        return guns

    def get_all_dresses(self) -> List[str]:
        """Get all available dresses"""
        return [str(dress) for dress in self.dresses]

    def simulate_battle(self, attacker: Character, defender: Character) -> Dict:
        """Simulate a battle between two characters"""
        if not attacker.current_weapon:
            return {"winner": None, "message": "Attacker has no weapon equipped"}

        damage = attacker.current_weapon["damage"] + random.randint(-10, 10)
        defender.take_damage(damage)

        result = {
            "attacker": attacker.name,
            "defender": defender.name,
            "damage_dealt": damage,
            "defender_health": defender.health,
            "winner": attacker.name if defender.health <= 0 else None
        }
        return result

    def __repr__(self):
        return f"GameManager: {len(self.characters)} characters, {len(self.lobbies)} lobbies"


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("GAME MANAGEMENT SYSTEM")
    print("=" * 60)

    # Initialize game manager
    game = GameManager()
    print(f"\n{game}\n")

    # Create characters
    print("Creating Characters...")
    char1 = game.create_character("Hero", "Warrior")
    char2 = game.create_character("Archer", "Archer")
    char3 = game.create_character("Mage", "Mage")
    char4 = game.create_character("Shadow", "Assassin")

    for char in [char1, char2, char3, char4]:
        print(f"  ✓ {char}")

    # Create lobby
    print("\nCreating Lobby...")
    lobby = game.create_lobby(max_players=4)
    print(f"  ✓ {lobby}")

    # Add players to lobby
    print("\nAdding Players to Lobby...")
    for char in [char1, char2, char3, char4]:
        if lobby.add_player(char):
            print(f"  ✓ {char.name} joined")

    # Add dresses to characters
    print("\nEquipping Dresses...")
    dress1 = game.dresses[0]
    dress2 = game.dresses[5]
    char1.add_dress(dress1)
    char1.equip_dress(dress1)
    print(f"  ✓ {char1.name} equipped: {char1.current_dress}")

    char2.add_dress(dress2)
    char2.equip_dress(dress2)
    print(f"  ✓ {char2.name} equipped: {char2.current_dress}")

    # Add weapons to characters
    print("\nEquipping Weapons...")
    char1.add_weapon(GunType.ASSAULT_RIFLE)
    char1.equip_weapon("Assault Rifle")
    print(f"  ✓ {char1.name} equipped: {char1.current_weapon['name']}")

    char2.add_weapon(GunType.SNIPER)
    char2.equip_weapon("Sniper Rifle")
    print(f"  ✓ {char2.name} equipped: {char2.current_weapon['name']}")

    # Show all available weapons
    print("\nAll 20 Available Guns:")
    for i, gun in enumerate(game.get_all_guns(), 1):
        print(f"  {i}. {gun['name']} - Damage: {gun['damage']}, Ammo: {gun['ammo']}")

    # Show all available dresses
    print(f"\nAll Available Dresses ({len(game.dresses)}):")
    for dress in game.dresses:
        print(f"  • {dress}")

    # Simulate a battle
    print("\nSimulating Battle...")
    result = game.simulate_battle(char1, char2)
    print(f"  {result['attacker']} attacked {result['defender']}")
    print(f"  Damage: {result['damage_dealt']}")
    print(f"  {result['defender']}'s health: {result['defender_health']}")

    # Lobby status
    print(f"\nLobby Status: {lobby}")
    print(f"  Players: {[p.name for p in lobby.players]}")
    print(f"  Ready to start: {lobby.is_ready()}")

    print("\n" + "=" * 60)
