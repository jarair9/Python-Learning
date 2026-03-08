from fileinput import filename
import os 

essay = "Projects\Texts\essay.txt"

def len_of_essay():
    with open(essay,encoding="utf-8",mode="r") as f:
        text = f.read()
        words = text.split()
        return len(words)
    
def len_of_letters():
    with open(essay,encoding="utf-8",mode="r") as f:
        text = f.read()
        return len(text)
    

def read_lines() -> list:
    """Search for a word in 'essay.txt' and return matching lines."""
    
    search = input("Enter word to search for: ")
    
    try:
        with open(essay,encoding="utf-8",mode="r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    
    matches = []
    for line in lines:
        if search.lower() in line.lower():
            matches.append(line.strip())
    
    return matches

# Call the function
results = read_lines()

# Display results
if results:
    print("Found matching lines:")
    for line in results:
        print(line)
else:
    print("No matches found.")