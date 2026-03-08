# Correct infinite loops:

# 1. Using while:
# while True:
    # print("Hello Computer")

# 2. Using for loop (with iterable):
from itertools import cycle
for _ in cycle([0]):
    print("Hello Computer")

# 3. Another for loop trick:
for _ in iter(int, 1):  # iter calls int() until it returns 1 (never)
    print("Hello Computer")

# But truth is: 
# For loops are designed for finite sequences. 
# For infinite loops, while True: is the standard way.