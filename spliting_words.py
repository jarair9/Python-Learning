

script = "script.txt"
with open(script,encoding= "utf-8",mode="r") as f:
    content = f.read()

print(len(content))    