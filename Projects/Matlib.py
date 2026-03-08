import os 


def matlib():
    start = ">"
    end = "<"
    checks = 0
    words = set()

    with open("Projects/story.txt","r",encoding="utf-8") as f:
        story = f.read()


    for i , j in enumerate(story): # show index and value
        if start in story:
            checks = i      # it will add start index
        elif end in story and checks != 0:
            finds = story[checks:i+1] 
            words.add(finds)
            checks = 0

    answer ={}

    for word in words:
        inputs = str(input(f"Enter a {word} name: "))
        words[word] = answer

    for word in words:
        story = story.replace(words,answer[word]) 
        print(story)    
            



        
    
if __name__ == "__main__":    
    matlib()
