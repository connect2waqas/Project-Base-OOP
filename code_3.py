from abc import ABC, abstractmethod
import random
class Character(ABC):
    def __init__(self, name : str, health : int, level : int):
        self.__inventory = Inventory(capacity=10)

        if not isinstance(name,str):
            raise TypeError("name must be string")
        self.__name = name.strip()

        if isinstance(health, (int,float)):
            self.__health = health
        if isinstance(level, int):
            self.__level = level
        else:
            raise TypeError("Invalid Datatype")
        
    @abstractmethod
    def attack(self):
        pass

    def take_damage(self, dmg: int):
        self.__health = max(0, self.__health - dmg)
        print(f"{self.__name} takes {dmg} damage. Health: {self.__health}")

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,name):
        if isinstance(name,str):
            self.__name = name
        else:
            raise TypeError("name should be String")
        
    @property
    def get_health(self):
        return self.__health
    
    @property
    def get_level(self):
        return self.__level
    # Add to Character
    @property
    def get_inventory(self):
        return self._Character__inventory

    @abstractmethod
    def __str__(self):
        pass

class Warrior(Character):
    def __init__(self, name: str, health: int, level: int, armor: int, rage: int):
        super().__init__(name, health, level)

        if not isinstance(armor, int):
            raise TypeError("armor must be integer")
        if armor < 0:
            raise ValueError("armor cannot be negative")

        if not isinstance(rage, int):
            raise TypeError("rage must be integer")
        if rage < 0:
            raise ValueError("rage cannot be negative")
        self.__armor = armor
        self.__rage = rage
    @property
    def armor(self)-> int:
        return self.__armor
    
    @armor.setter
    def armor(self, armor : int):
        if isinstance(armor,int):
            self.__armor += armor
        else:
            raise TypeError("Aromor should be integer")
        
    @property
    def rage(self):
        return self.__rage
    
    @rage.setter
    def rage(self, rage):
        if isinstance(rage, int):
            self.__rage += rage
        else:
            raise TypeError("invalid data types")
    def attack(self):
        print("Attack by Warrior")

    def take_damage(self, dmg : int):
        reduced = max(0,dmg - self.armor)
        super().take_damage(reduced)
        self.__rage = min(100,self.__rage + 10)

    def shield_block(self):
        self.__armor += 15
        print(f"{self.name} raises shield! Armor is now {self.__armor}")

    def berserker_rage(self) -> int:
        burst = self.__rage * 2
        self.__rage = 0
        return burst
    
    def __str__(self):
        return f"warrior : {self.name}\nHealth: {self.get_health}\nLevel: {self.get_level}\nArmor: {self.armor}\nRage: {self.rage}"

class Spell:
    def __init__(self, name: str, mana_cost: int, spell_power: int):
        self.__name = name
        self.__mana_cost = mana_cost
        self.__spell_power = spell_power
    @property
    def get_name(self) -> str:
        return self.__name
    
    @property
    def get_mana_cost(self) -> int:
        return self.__mana_cost

    def cast(self) -> int:
        print(f"{self.__name} cast! Deals {self.__spell_power} damage.")
        return self.__spell_power

    def describe(self) -> str:
        return f"{self.__name} | Cost: {self.__mana_cost} mana | Power: {self.__spell_power}"

class Mage(Character):

    MAX_MANA = 100

    def __init__(self, name: str, health: int, level:int):
        super().__init__(name, health, level)
        self.__mana = self.MAX_MANA
        self.__spells = []

    @property
    def get_mana(self):
        return self.__mana

    def learn_spell(self, spell):
        self.__spells.append(spell)

    def attack(self):
        cost = 5
        if self.__mana < cost:
            print("Not enough mana for basic attack")
            return 0
        return 10
    
    def take_damage(self, dmg):
        if self.__mana >= dmg:
            self.__mana -= dmg
            print(f"Mana sheild absorb {dmg} damage! mana {self.get_mana}")
        elif self.__mana > 0:
            remaining = dmg - self.__mana
            print(f"Mana shield absorbs {self.__mana} damage.")
            self.__mana = 0
            super().take_damage(remaining)
        else:
            super().take_damage(dmg)

    def cast_spell(self, spell):
        if self.__mana < spell.get_mana_cost:
            print(f"Not enough mana to cast {spell.get_name()}!")
            return 0
        self.__mana -= spell.get_mana_cost
        return spell.cast()

    def restore(self):
        self.__mana = min(self.MAX_MANA, self.__mana + 30)
        print(f"Mana restored. Current mana: {self.__mana}")

    def __str__(self):
        return f"warrior : {self.name}\nHealth: {self.get_health}\nLevel: {self.get_level}\nMana : {self.get_mana}\nMaximum Mana {self.MAX_MANA}\n"
    
class Rogue(Character):
    def __init__(self, name: str, health: int, level: int):
        super().__init__(name, health, level)
        self.__agility = 20
        self.__stealth = False

    @property
    def get_agility(self) -> int:
        return self.__agility

    def is_stealthed(self) -> bool:
        return self.__stealth

    def take_damage(self, dmg: int):
        dodge_chance = self.__agility // 10   
        if random.randint(1, 100) <= dodge_chance:
            print(f"{self.get_name()} dodged the attack!")
            return
        self.__stealth = False                
        super().take_damage(dmg)

    def attack(self) -> int:
        hits = self.__agility // 10       
        damage_per_hit = 8
        total = hits * damage_per_hit
        print(f"{self.name} strikes {hits}x for {total} total damage.")
        return total

    def sneak(self):
        self.__stealth = True
        print(f"{self.name} vanishes into the shadows.")

    def backstab(self) -> int:
        if not self.__stealth:
            print("Must be in stealth to backstab!")
            return 0
        self.__stealth = False              
        critical = 40
        print(f"{self.name} backstabs for {critical} critical damage!")
        return critical
    
    def __str__(self):
        return f"warrior : {self.name}\nHealth: {self.get_health}\nLevel: {self.get_level}\nAgilty : {self.get_agility}"

class Weapon:
    def __init__(self, name: str, dmg: int, weapon_type : str):
        self.__name = name
        self.__dmg = dmg
        self.__weapon_type = weapon_type
    @property
    def get_name(self):
        return self.__name
    
    @property
    def get_damage(self)-> int:
        return self.__dmg
    @property
    def get_type(self):
        return self.__weapon_type
    
    def describe(self):
        return f"{self.get_name} | Type : {self.get_type} | Damage : {self.get_damage}"
    # Add to Weapon
    def __str__(self):
        return f"{self.get_name} | Type : {self.get_type} | Damage : {self.get_damage}"
class Inventory:
    def __init__(self, capacity: int):
        self.__items = []
        self.__capacity = capacity

    def add_item(self, weapon):
        if len(self.__items) < self.__capacity:
            self.__items.append(weapon)
        else:
            print("Inventory is full!")

    def remove_item(self, weapon):
        if weapon in self.__items:
            self.__items.remove(weapon)
        else:
            print(f"{weapon} does not exit")

    def show_items(self):
        for i in self.__items:
            print(i)
    
    def is_full(self) -> bool:
        return len(self.__items) >= self.__capacity

print("=" * 50)
print("TEST 1: Weapon class")
print("=" * 50)

sword  = Weapon("Sword", 30, "melee")
bow    = Weapon("Bow", 20, "ranged")
dagger = Weapon("Dagger", 15, "melee")
print(sword)
print(sword.describe())    # Sword | Type : melee | Damage : 30
print(bow.describe())      # Bow | Type : ranged | Damage : 20
print(dagger.describe())   # Dagger | Type : melee | Damage : 15

print("\n" + "=" * 50)
print("TEST 2: Spell class")
print("=" * 50)

fireball = Spell("Fireball", 20, 50)
ice_bolt = Spell("Ice Bolt", 10, 25)

print(fireball.describe())   # Fireball | Cost: 20 mana | Power: 50
print(ice_bolt.describe())   # Ice Bolt | Cost: 10 mana | Power: 25
print(fireball.cast())       # Fireball cast! Deals 50 damage. → 50

print("\n" + "=" * 50)
print("TEST 3: Inventory class")
print("=" * 50)

inv = Inventory(capacity=2)
inv.add_item(sword)
inv.add_item(bow)
inv.show_items()             # Sword, Bow
inv.add_item(dagger)         # Inventory is full!
inv.remove_item(sword)
inv.show_items()             # Bow only
print(inv.is_full())         # False
inv.add_item(dagger)
print(inv.is_full())         # True

print("\n" + "=" * 50)
print("TEST 4: Warrior class")
print("=" * 50)

w = Warrior("Thor", 100, 1, armor=10, rage=0)
print(w)                          # warrior info
w.get_inventory.add_item(sword)
w.get_inventory.show_items()      # Sword listed
w.take_damage(25)                 # reduced by armor: 25-10=15, health→85, rage→10
print(f"Rage after hit: {w.rage}")           # 10
print(f"Health after hit: {w.get_health}")   # 85
w.shield_block()                  # armor raises by 15 → 25
w.take_damage(20)                 # reduced by armor: 20-25=0, health stays 85
print(f"Burst damage: {w.berserker_rage()}")  # 10*2=20, rage resets to 0
print(f"Rage after burst: {w.rage}")          # 0

print("\n" + "=" * 50)
print("TEST 5: Mage class")
print("=" * 50)

m = Mage("Gandalf", 80, 1)
print(m)                          # mage info
m.learn_spell(fireball)
m.learn_spell(ice_bolt)
print(f"Mana before: {m.get_mana}")     # 100
print(f"Basic attack: {m.attack()}")    # 10 damage, costs 5 mana
print(f"Mana after basic: {m.get_mana}") # 95
print(m.cast_spell(fireball))    # Fireball cast! → 50, mana→75
m.take_damage(30)                # mana absorbs: mana→45, health→80
m.take_damage(60)                # mana absorbs 45, remaining 15 hits health→65
m.take_damage(10)                # no mana → health→55
m.restore()                      # mana→75
print(f"Mana after restore: {m.get_mana}")  # 75

print("\n" + "=" * 50)
print("TEST 6: Rogue class")
print("=" * 50)

r = Rogue("Shadow", 75, 1)
print(r)                          # rogue info
print(f"Attack damage: {r.attack()}")   # 2 hits x 8 = 16
print(r.backstab())               # Must be in stealth → 0
r.sneak()                         # stealth = True
print(r.backstab())               # 40 critical damage, stealth broken
print(r.backstab())               # Must be in stealth → 0
r.take_damage(20)                 # 20% dodge chance, else takes 20

print("\n" + "=" * 50)
print("TEST 7: Polymorphism — same attack() call, different behavior")
print("=" * 50)

characters = [
    Warrior("Thor", 100, 1, armor=10, rage=50),
    Mage("Gandalf", 80, 1),
    Rogue("Shadow", 75, 1)
]
for c in characters:
    print(f"{c.name} attacks → {c.attack()}")
# Warrior: weapon+rage based
# Mage: 10 magic bolt
# Rogue: 2x8 = 16

print("\n" + "=" * 50)
print("TEST 8: Abstraction — cannot instantiate Character directly")
print("=" * 50)

try:
    c = Character("Test", 100, 1)
except TypeError as e:
    print(f"Caught expected error: {e}")
# Expected: Can't instantiate abstract class