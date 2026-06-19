from abc import ABC, abstractmethod
import random
class Character(ABC):
    def __init__(self, name : str, health : int, level : int, inventry=[123]):
        if isinstance(name.strip(),str):
            self.__name = name
        if isinstance(health, (int,float)):
            self.__health = health
        if isinstance(level, int):
            self.__level = level
        if isinstance(inventry,list):
            self.__inventry = inventry
        else:
            raise TypeError("Invalid Datatype")
        
    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def take_damage(self, dmg):
        pass

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

    @abstractmethod
    def __str__(self):
        pass

class Warrior(Character):
    def __init__(self, name: str, health: int, level: int, inventry: None, armor: int, rage: int):
        super().__init__(name, health, level, inventry)

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
        print(f"{self.get_name()} raises shield! Armor is now {self.__armor}")

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
        dodge_chance = self.__agility // 10    # agility 20 = 20% dodge
        if random.randint(1, 100) <= dodge_chance:
            print(f"{self.get_name()} dodged the attack!")
            return
        self.__stealth = False                 # getting hit breaks stealth
        super().take_damage(dmg)

    def attack(self) -> int:
        hits = self.__agility // 10            # agility 20 = 2 hits
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
        self.__stealth = False                 # breaks stealth after use
        critical = 40
        print(f"{self.name} backstabs for {critical} critical damage!")
        return critical
    
    def __str__(self):
        return f"warrior : {self.name}\nHealth: {self.get_health}\nLevel: {self.get_level}\nAgilty : {self.get_agility}"
    
r = Rogue("Shadow", 75, 1)

print(r.attack())       # 2 hits x 8 = 16 total damage
r.sneak()               # stealth = True
print(r.backstab())     # 40 critical damage, stealth = False
print(r.backstab())     # "Must be in stealth" → returns 0
r.take_damage(20)       # 20% chance to dodge, else takes 20 damage