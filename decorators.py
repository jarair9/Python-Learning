

def my_decorator(func):
    print(f"I just saw a function called: {func.__name__}")
    return func  # must return the function back!

@my_decorator
def say_hello():
    print("Hello!")

# Output when Python reads the file:
# "I just saw a function called: say_hello"

# @my_decorator is just a shortcut for:
# say_hello = my_decorator(say_hello)  # same thing!

registry = {}  # empty dict

def register(func):
    registry[func.__name__] = func  # save function by its name
    return func

@register
def eat():
    print("eating!")

@register
def sleep():
    print("sleeping!")

print(registry)
# {'eat': <function eat>, 'sleep': <function sleep>}  ✅ automatic!

registry = {}

def tool(description):       # outer function takes your arguments
    def decorator(func):     # inner function takes the function
        registry[func.__name__] = {
            "function": func,
            "description": description
        }
        return func
    return decorator         # must return decorator!

@tool(description="Says hello to someone")
def say_hello():
    print("Hello!")

@tool(description="Says goodbye to someone")
def say_bye():
    print("Bye!")

print(registry)
# {
#   'say_hello': {'function': <func>, 'description': 'Says hello to someone'},
#   'say_bye':   {'function': <func>, 'description': 'Says goodbye to someone'}
# }