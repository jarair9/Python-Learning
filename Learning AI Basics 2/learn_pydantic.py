from pydantic import BaseModel

# This is a "model" - think of it as a template or blueprint
class Person(BaseModel):
    name: str      # Must be a string
    age: int       # Must be an integer
    email: str     # Must be a string

# Now let's use it
print("=== Example 1: Correct Data ===")
person1 = Person(
    name="Ali",
    age=25,
    email="ali@example.com"
)
print(f"Name: {person1.name}")
print(f"Age: {person1.age}")
print(f"Email: {person1.email}")
print(f"Whole person: {person1}")