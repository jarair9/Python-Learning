# ================================================================================
# A decorator is just a function that takes another function and returns something
# ================================================================================

def text(func):
    print("hello friend")
    func()
    print("bye friend")

def friend_name():
    print("Jarair bro")

text(friend_name)

print() # for Space

def wrapper(func):
    def new_func():
        print("Before")
        func()
        print("After")
    return new_func


def greet():
    print("Hello")

greet = wrapper(greet)

greet()