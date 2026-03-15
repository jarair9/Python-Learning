import os 
import shutil


class Filehandler:
    def __init__(self,path):
        self.path = path
    
    def handler(self):
        items = os.listdir(self.path)

        formats = {
    "images": [
        ".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp", ".tiff", 
        ".tif", ".raw", ".cr2", ".nef", ".heic", ".heif", ".ico", ".psd", 
        ".ai", ".eps", ".pdf", ".jfif"
    ],
    "videos": [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", 
        ".mpeg", ".mpg", ".3gp", ".ts", ".m2ts", ".vob", ".ogv"
    ],
    "audio": [  # expanded from "Voice"
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff", 
        ".au", ".ra", ".ram", ".opus", ".weba"
    ],
    "documents": [
        ".doc", ".docx", ".txt", ".rtf", ".odt", ".pdf", ".md", ".tex", 
        ".pages", ".wpd"
    ],
    "spreadsheets": [
        ".xls", ".xlsx", ".csv", ".ods", ".tsv", ".numbers"
    ],
    "presentations": [
        ".ppt", ".pptx", ".odp", ".key", ".pps", ".ppsx"
    ],
    "archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", 
        ".dmg", ".pkg", ".deb", ".rpm"
    ],
    "code": [
        ".html", ".css", ".js", ".py", ".java", ".cpp", ".c", ".h", ".php", 
        ".rb", ".go", ".swift", ".json", ".xml", ".yaml", ".sql", ".crdownload",".har"
    ],
    "fonts": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot"
    ],
    "executables": [
        ".exe", ".msi", ".app", ".dmg", ".deb", ".rpm", ".sh", ".bat"
    ]
}


        for item in items:
            item_dir = os.path.join(self.path,item)  
            print(f"\nProcessing: {item_dir}")

            

            if os.path.isdir(item_dir):
                print(f"\nSkipping directory: {item_dir}")
                continue

            ext = os.path.splitext(item)[1].lower() # get the file extension and convert to lowercase for case-insensitive matching

            for i in formats: 
                if ext in formats[i]: 
                    if not os.path.exists(os.path.join(self.path,i)):
                        os.makedirs(os.path.join(self.path,i))
                   
                    try: 
                        shutil.move(item_dir, os.path.join(self.path,i, item))
                        print(f"Moved {item} to {i} folder.")
                    except Exception as e:
                        print(f"Error moving {item}: {e}")
                else:
                    print(f"No matching folder for extension: {ext}")
                    

s = Filehandler(r"")
s.handler()
        

                    
                


            
        
