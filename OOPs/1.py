
class Animal:
    def __init__(self,name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")

    def sleep(self):
        print(f"{self.name} is sleeping.")


class Prey(Animal):
    def caught(self):
        print(f"{self.name} is hunted")

class Predator(Animal):
    def hunt(self):
        print(f"{self.name} do hunt")

class Dog(Predator):
    pass

class Cat(Prey):
    pass

class Fish(Prey,Predator):
    pass



# Demonstrate all methods
dog = Dog("Puppy")
cat = Cat("moew")
fish = Fish("hanker")

print("=== Dog (Predator only) ===")
dog.sleep()    # From Animal
dog.eat()      # From Animal  
dog.hunt()     # From Predator
# dog.caught() # Not available

print("\n=== Cat (Prey only) ===")
cat.sleep()    # From Animal
cat.eat()      # From Animal
cat.caught()   # From Prey
# cat.hunt()   # Not available

print("\n=== Fish (Both Prey and Predator) ===")
fish.sleep()   # From Animal
fish.eat()     # From Animal
fish.hunt()    # From Predator
fish.caught()  # From Prey