# Creating Program that Cleans the AI Scripts and Prompts that feel real not AI Generated.
# humanixing the AI Masseges require changing tone (But we only remove AI random Place holders, Symbols.)


def cleaner(file):
    """
    Cleaning AI Script and Prompts
    Input Arg: FIle Path
    OutPut Result: clean Script
    """
    with open(file,"r") as f:
        content = f.read()

    symbols = ["_","-","[","]","*","`","█","#","✅","❌"]

    for char in content:
        if symbols in char:
            content = content.replace(char,"") # replacing with nothing (So it will remove)

    with open(file,encoding="utf-8",mode="w") as f:
        f.write(content)

    print("Successfully Cleaned Up The File")



# Cleaner Function takes an FIle path or name.
# Just add file name if that file exist in same dir where this program exist.
cleaner()
    