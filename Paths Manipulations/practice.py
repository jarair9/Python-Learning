import shutil
import os


dir_path = r"C:\Users\Shaheen Alam\Pictures"
items = os.listdir(dir_path)


def organize_images():
    
    
    # Check if path exists
    if not os.path.exists(dir_path):
        print(f"❌ Path does not exist: {dir_path}")
        return
    
    
    
    # Create Images directory if it doesn't exist
    images_dir = os.path.join(dir_path, "Images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir, exist_ok=True)
        print(f"✅ Created directory: {images_dir}")
    
    
    
    for item in items:
        # Get full path of the item
        item_path = os.path.join(dir_path, item)
        
        # Skip if it's a directory (not a file)
        if os.path.isdir(item_path):
            continue
        
        # Check file extension
        if item.lower().endswith((".png", ".jpeg", ".jpg")):
            # Create destination path
            destination = os.path.join(images_dir, item)
            
            try:
                shutil.move(item_path, destination)
                print(f"✅ Moved: {item}")
                
            except Exception as e:
                print(f"❌ Failed to move {item}: {e}")
    
    print(f"\n📊 Moved  image files to {images_dir}")



def organize_audio():

    audio_dir = os.path.join(dir_path, "Audio")
    text_dir = os.path.join(dir_path, "Text")


    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir, exist_ok=True)
        print(f"✅ Created directory: {audio_dir}")
    

    if not os.path.exists(text_dir):
        os.makedirs(text_dir, exist_ok=True)
        print(f"✅ Created directory: {text_dir}")

    for itms in items:
        itms_path = os.path.join(dir_path,itms)

        if os.path.isdir(itms_path):
            continue

        if itms.lower().endswith((".mp3", ".wav")):
            destination = os.path.join(audio_dir, itms)

            try:
                shutil.move(itms_path, destination)
                print(f"✅ Moved: {itms}")
                
            except Exception as e:
                print(f"❌ Failed to move {itms}: {e}")
        
        elif itms.lower().endswith((".txt", ".docx",".py")):

            destination = os.path.join(text_dir, itms)

            try:
                shutil.move(itms_path, destination)
                print(f"✅ Moved: {itms}")
                
            except Exception as e:
                print(f"❌ Failed to move {itms}: {e}")

        print(f"\n📊 Moved  image files to {audio_dir} and text files to {text_dir} ")

        
if __name__ == "__main__":
    organize_images()
    organize_audio()
    
    
   