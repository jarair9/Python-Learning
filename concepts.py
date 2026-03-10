# checking if the dict can be iterateable



my_dict = {'a': 1, 'b': 2, 'c': 3}
for key in my_dict:
    print(f"Key: {key}, Value: {my_dict[key]}")


#list iteration
same = ""
strs = ["flower","flow","flight"]
for i in strs: # == flower, flow, flight
    for char in i: # == f, l, o, w, e, r ...
        print(char)

s = "aaabaaa"
k = 3

n = len(s)
        
for i in range(n - k + 1):# Extract the substring of length k
    substring = s[i:i + k] # 
    print(substring)





a = '1010'
b = '101'


i = len(a) - 1 
print(i)


dic = {}
keys = ["a", "b", "c"]
values = [1, 2, 3]

for i in range(len(keys)):
    dic[keys[i]] = values[i]

print(dic)




print()



roman_values = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
s = "MCMXCIV"        
# Iterate through the string in reverse
for char in s[::-1]:
    value = roman_values[char]
print(value)
print()
strs = ["flower","flow","flight"]
prefix = strs[0]
prefix2 = strs[1:]
prefix3 = strs[:-1]
print(prefix)
print(prefix2)
print(prefix3)

formats = {
            "images": [".jpg",".png",".jpeg",".svg"],
            "Videos": [".mp4"],
            "Doc": [".doc",".txt",],
            "Voice": [".wav",".mp3"]
        }

for i in formats:
    print(formats[i])


print()

import random
size = random.randint(100, 250)
print(size)



print(random.randint(0,800))



    

# /   → decimal answer
# //  → whole number answer
# %   → remainder