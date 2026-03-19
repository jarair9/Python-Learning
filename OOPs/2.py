
# AI Generated for Learning Purposes


from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# Abc = Abstract Class

# Abstruct clases canot work alone without child. WHen we define 
# method in Abstruct class we cannot excess it from that Class we should 
# create another Class and inherete the Abstruct call and create and complete 
# Methods And call the child class so it would run sucessfully.
 

# ============= BASE CLASSES (Multilevel Inheritance Starting Point) =============
class LivingBeing(ABC):
    """Base class for all living things"""
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.alive = True
        self.energy = 100
        self.created_at = datetime.now()
    
    @abstractmethod
    def make_sound(self):
        """Abstract method - each living being makes its own sound"""
        pass
    
    def breathe(self):
        if self.alive:
            print(f"{self.name} is breathing. Energy +5")
            self.energy += 5
            return True
        return False
    
    def age_progress(self, days=1):
        self.age += days
        self.energy -= days * 2
        if self.energy <= 0:
            self.alive = False
            print(f"{self.name} has passed away at age {self.age}")
        return self.age

# Multilevel: LivingBeing → Animal
class Animal(LivingBeing):
    def __init__(self, name, age, species, habitat):
        super().__init__(name, age)
        self.species = species
        self.habitat = habitat
        self.hunger = 0
        self.thirst = 0
    
    def eat(self, food_amount=10):
        if self.alive:
            print(f"{self.name} is eating. Hunger -{food_amount}")
            self.hunger = max(0, self.hunger - food_amount)
            self.energy += food_amount // 2
            return True
        return False
    
    def drink(self, water_amount=5):
        if self.alive:
            print(f"{self.name} is drinking. Thirst -{water_amount}")
            self.thirst = max(0, self.thirst - water_amount)
            self.energy += water_amount // 2
            return True
        return False
    
    def move(self, distance):
        if self.alive and self.energy > distance:
            print(f"{self.name} moves {distance} meters")
            self.energy -= distance
            self.hunger += distance // 10
            self.thirst += distance // 15
            return True
        return False

# ============= MIXINS (For Multiple Inheritance) =============
class FlyableMixin:
    """Mixin for flying capabilities"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wings = 2
        self.max_altitude = 100
    
    def fly(self, altitude):
        if hasattr(self, 'energy') and self.energy >= altitude:
            print(f"{self.name} is flying at {altitude} meters")
            self.energy -= altitude // 2
            return True
        return False
    
    def land(self):
        print(f"{self.name} is landing")
        return True

class SwimmableMixin:
    """Mixin for swimming capabilities"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fins = True
        self.swim_speed = 10
    
    def swim(self, distance):
        if hasattr(self, 'energy') and self.energy >= distance:
            print(f"{self.name} is swimming {distance} meters")
            self.energy -= distance // 2
            return True
        return False
    
    def dive(self, depth):
        print(f"{self.name} dives to {depth} meters deep")
        return True

class ClimbableMixin:
    """Mixin for climbing capabilities"""
    def climb(self, height):
        if hasattr(self, 'energy') and self.energy >= height * 2:
            print(f"{self.name} climbs {height} meters")
            self.energy -= height * 2
            return True
        return False

# ============= MULTILEVEL INHERITANCE CHAIN =============
# Level 1: Animal → Mammal
class Mammal(Animal):
    def __init__(self, name, age, species, habitat, fur_color):
        super().__init__(name, age, species, habitat)
        self.fur_color = fur_color
        self.pregnant = False
    
    def give_birth(self):
        if self.pregnant:
            print(f"{self.name} gives birth to live young")
            self.pregnant = False
            return BabyMammal(f"Baby {self.name}", 0, self.species, self.habitat, self.fur_color)
        return None
    
    def nurse(self, baby):
        if hasattr(baby, 'energy'):
            print(f"{self.name} nurses {baby.name}")
            baby.energy += 30
            self.energy -= 10

# Level 2: Mammal → Primate
class Primate(Mammal):
    def __init__(self, name, age, species, habitat, fur_color, brain_size):
        super().__init__(name, age, species, habitat, fur_color)
        self.brain_size = brain_size
        self.opposable_thumbs = True
    
    def use_tool(self, tool):
        if self.opposable_thumbs:
            print(f"{self.name} uses a {tool} as a tool")
            self.energy -= 5
            return True
        return False
    
    def make_sound(self):
        return f"{self.name} chatters and gestures"

# Level 3: Primate → Ape
class Ape(Primate):
    def __init__(self, name, age, species, habitat, fur_color, brain_size, social_group):
        super().__init__(name, age, species, habitat, fur_color, brain_size)
        self.social_group = social_group
        self.grooming_partners = []
    
    def groom(self, other_ape):
        if other_ape in self.grooming_partners:
            print(f"{self.name} grooms {other_ape.name}")
            self.energy -= 3
            other_ape.energy += 5
            return True
        return False
    
    def make_sound(self):
        return f"{self.name} hoots loudly to the {self.social_group} group"

# ============= MULTIPLE INHERITANCE EXAMPLES =============
class Bat(Mammal, FlyableMixin):
    """Bat inherits from Mammal (multilevel) and FlyableMixin"""
    def __init__(self, name, age, fur_color, nocturnal=True):
        Mammal.__init__(self, name, age, "Bat", "Caves", fur_color)
        FlyableMixin.__init__(self)
        self.nocturnal = nocturnal
        self.echolocation = True
    
    def make_sound(self):
        return f"{self.name} emits high-frequency clicks"
    
    def echo_locate(self):
        if self.echolocation:
            print(f"{self.name} uses echolocation to find prey")
            self.energy -= 2

class Duck(Animal, FlyableMixin, SwimmableMixin):
    """Duck inherits from Animal and two mixins"""
    def __init__(self, name, age, species="Mallard"):
        Animal.__init__(self, name, age, species, "Wetlands")
        FlyableMixin.__init__(self)
        SwimmableMixin.__init__(self)
        self.webbed_feet = True
        self.max_altitude = 500
    
    def make_sound(self):
        return "Quack quack!"
    
    def fly_and_swim(self):
        """Demonstrates using multiple inherited capabilities"""
        print(f"{self.name} takes off from water")
        self.fly(10)
        print(f"{self.name} lands on water")
        self.swim(20)

class Frog(Animal, SwimmableMixin, ClimbableMixin):
    """Frog inherits from Animal and multiple mixins"""
    def __init__(self, name, age, species="Tree Frog"):
        Animal.__init__(self, name, age, species, "Rainforest")
        SwimmableMixin.__init__(self)
        ClimbableMixin.__init__(self)
        self.metamorphosis_complete = True
    
    def make_sound(self):
        return "Ribbit ribbit!"
    
    def jump(self, distance):
        if self.energy >= distance:
            print(f"{self.name} jumps {distance} meters!")
            self.energy -= distance // 2
            return True
        return False

class Platypus(Mammal, SwimmableMixin):
    """Platypus - mammal that swims (unique multiple inheritance)"""
    def __init__(self, name, age, fur_color):
        Mammal.__init__(self, name, age, "Platypus", "Rivers", fur_color)
        SwimmableMixin.__init__(self)
        self.venomous_spur = True
        self.lays_eggs = True  # Exception to mammal rule!
    
    def make_sound(self):
        return f"{self.name} makes a soft growl"
    
    def lay_egg(self):
        if self.lays_eggs:
            print(f"{self.name} lays an egg!")
            return Egg("Platypus Egg", self.name)

# Helper class
class Egg:
    def __init__(self, species, parent):
        self.species = species
        self.parent = parent
        self.laid_at = datetime.now()
        self.hatches_in = timedelta(days=10)
    
    def hatch(self):
        if datetime.now() > self.laid_at + self.hatches_in:
            return Platypus(f"Baby {self.parent}", 0, "Brown")
        return None

class BabyMammal(Mammal):
    """Baby mammals (demonstrates inheritance chain)"""
    def __init__(self, name, age, species, habitat, fur_color):
        super().__init__(name, age, species, habitat, fur_color)
        self.dependent = True
    
    def make_sound(self):
        return f"{self.name} makes tiny squeaking sounds"

# ============= DEMONSTRATION =============
def demonstrate_inheritance():
    print("=" * 60)
    print("ZOO MANAGEMENT SYSTEM - INHERITANCE DEMONSTRATION")
    print("=" * 60)
    
    # 1. Multilevel Inheritance Example (Ape)
    print("\n--- MULTILEVEL INHERITANCE: Ape from LivingBeing → Animal → Mammal → Primate → Ape ---")
    gorilla = Ape("Kong", 15, "Gorilla", "Jungle", "Black", 500, "Silverback")
    print(f"Created: {gorilla.name}, Species: {gorilla.species}, Age: {gorilla.age}")
    print(f"Has fur? {gorilla.fur_color} fur")
    print(f"Has opposable thumbs? {gorilla.opposable_thumbs}")
    print(f"Social group: {gorilla.social_group}")
    print(f"Sound: {gorilla.make_sound()}")
    
    # Add grooming partner
    chimp = Ape("Cheetah", 10, "Chimpanzee", "Jungle", "Brown", 400, "Troop")
    gorilla.grooming_partners.append(chimp)
    gorilla.groom(chimp)
    
    # 2. Multiple Inheritance Example (Bat)
    print("\n--- MULTIPLE INHERITANCE: Bat (Mammal + FlyableMixin) ---")
    bat = Bat("Bruce", 2, "Black")
    print(f"Created: {bat.name}, Type: {bat.species}")
    print(f"Is mammal? {isinstance(bat, Mammal)}")
    print(f"Can fly? {isinstance(bat, FlyableMixin)}")
    bat.breathe()
    bat.fly(30)
    bat.echo_locate()
    bat.land()
    print(f"Sound: {bat.make_sound()}")
    
    # 3. Multiple Inheritance with Two Mixins (Duck)
    print("\n--- MULTIPLE INHERITANCE: Duck (Animal + FlyableMixin + SwimmableMixin) ---")
    donald = Duck("Donald", 3)
    print(f"Created: {donald.name}, Species: {donald.species}")
    print(f"Can fly? {isinstance(donald, FlyableMixin)}")
    print(f"Can swim? {isinstance(donald, SwimmableMixin)}")
    print(f"Webbed feet? {donald.webbed_feet}")
    donald.fly_and_swim()
    print(f"Sound: {donald.make_sound()}")
    
    # 4. Another Multiple Inheritance (Frog)
    print("\n--- MULTIPLE INHERITANCE: Frog (Animal + SwimmableMixin + ClimbableMixin) ---")
    kermit = Frog("Kermit", 1)
    print(f"Created: {kermit.name}, Species: {kermit.species}")
    kermit.jump(5)
    kermit.swim(10)
    kermit.climb(3)
    print(f"Sound: {kermit.make_sound()}")
    
    # 5. Unusual Multiple Inheritance (Platypus)
    print("\n--- UNUSUAL MULTIPLE INHERITANCE: Platypus (Mammal + SwimmableMixin + Egg-laying) ---")
    perry = Platypus("Perry", 5, "Brown")
    print(f"Created: {perry.name}, Species: {perry.species}")
    print(f"Is mammal? {isinstance(perry, Mammal)} (but lays eggs!)")
    print(f"Can swim? {isinstance(perry, SwimmableMixin)}")
    print(f"Has venomous spur? {perry.venomous_spur}")
    perry.swim(25)
    egg = perry.lay_egg()
    print(f"Laid egg at: {egg.laid_at}")
    
    # 6. Method Resolution Order (MRO) Demonstration
    print("\n--- METHOD RESOLUTION ORDER ---")
    print("Duck MRO:")
    for i, cls in enumerate(Duck.__mro__):
        print(f"  Level {i}: {cls.__name__}")
    
    # 7. Testing isinstance and issubclass
    print("\n--- TYPE CHECKING ---")
    print(f"Is Duck an Animal? {issubclass(Duck, Animal)}")
    print(f"Is Duck a FlyableMixin? {issubclass(Duck, FlyableMixin)}")
    print(f"Is donald a SwimmableMixin? {isinstance(donald, SwimmableMixin)}")
    print(f"Is gorilla a Mammal? {isinstance(gorilla, Mammal)}")
    print(f"Is gorilla a Primate? {isinstance(gorilla, Primate)}")
    print(f"Is gorilla an Ape? {isinstance(gorilla, Ape)}")

# Run the demonstration
if __name__ == "__main__":
    demonstrate_inheritance()
    
    # Bonus: Show diamond inheritance problem (avoided with mixins)
    print("\n" + "=" * 60)
    print("BONUS: Diamond Inheritance Pattern")
    print("=" * 60)
    
    class Base:
        def method(self):
            return "Base"
    
    class Left(Base):
        def method(self):
            return "Left"
    
    class Right(Base):
        def method(self):
            return "Right"
    
    class Diamond(Left, Right):
        pass
    
    diamond = Diamond()
    print(f"Diamond method resolution: {diamond.method()} (from {Diamond.__mro__[1].__name__})")
    print("Python follows MRO - left to right, depth-first")