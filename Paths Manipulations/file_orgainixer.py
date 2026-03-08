import os
import shutil


# def searching_files():
#     paths = r"C:\Users\Shaheen Alam\Pictures"
#     items = os.listdir(paths)
    
#     files = []
#     directories = []
    
#     for item in items:
#         full_path = os.path.join(paths, item)
#         if os.path.isfile(full_path):
#             files.append(item)
#         elif os.path.isdir(full_path):
#             directories.append(item)
    
#     print(f"\nDirectory: {paths}")
#     print("-" * 50)
#     print(f"Directories ({len(directories)}):")
#     for d in sorted(directories):
#         print(f"  [DIR] {d}") 
    
#     print(f"\nFiles ({len(files)}):")
#     for f in sorted(files):
#         print(f"  [FILE] {f}")  

#     counts = 0
#     for dir_name in directories:
#     	dir_path= os.path.join(paths,dir_name)
#     	print(f"\n {dir_name}")
#     	elements = os.listdir(dir_path)

#     	for i in elements:
#     		itms = os.path.join(dir_path,i)
#     		if os.path.isfile(itms):
#     			print(f"{i}")
#     			counts += 1
#     		if os.path.isdir(itms):
#     			print(i)

#     print(f"Total files Tracked : {counts}")





def organize_files():
    paths = r"C:\Users\Shaheen Alam\Pictures"
    
    # Check if path exists
    if not os.path.exists(paths):
        print(f"❌ Path does not exist: {paths}")
        return
    
    items = os.listdir(paths)
    
    # Create Images directory if it doesn't exist
    images_dir = os.path.join(paths, "Images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir, exist_ok=True)
        print(f"✅ Created directory: {images_dir}")
    
    moved_count = 0
    
    for item in items:
        # Get full path of the item
        item_path = os.path.join(paths, item)
        
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
                moved_count += 1
            except Exception as e:
                print(f"❌ Failed to move {item}: {e}")
    
    print(f"\n📊 Moved {moved_count} image files to {images_dir}")

organize_files()