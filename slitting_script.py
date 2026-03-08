

# Cleaning AI Script from unwanted characters such as #, *, -, →, ←
script_file = "script.txt"
with open(script_file,encoding="utf-8",mode="r") as file:
    content = file.read()

for i in content:
    if i in ["#","*","—","→","←","-"]:
        content = content.replace(i,"")

with open(script_file,encoding="utf-8",mode="w") as file:    file.write(content)


    
