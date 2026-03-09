import shutil
from pathlib import Path

# === COPY FILES ===
# Copy single file
shutil.copy('source.txt', 'destination.txt')  # Basic copy
shutil.copy2('source.txt', 'dest.txt')  # Copy with metadata (timestamps)

# Copy with permissions
shutil.copy('src.txt', 'dst.txt')
shutil.copymode('src.txt', 'dst.txt')  # Copy permissions only
shutil.copystat('src.txt', 'dst.txt')  # Copy timestamps only

# === COPY DIRECTORIES ===
# Copy entire directory tree
shutil.copytree('source_folder', 'destination_folder')  # Both must not exist
shutil.copytree('src', 'dst', dirs_exist_ok=True)  # Python 3.8+: dst can exist

# Selective copying
def ignore_pycache(dirname, filenames):
    return ['.pycache', '__pycache__']  # Ignore these

shutil.copytree('src', 'dst', ignore=ignore_pycache)

# === MOVE/RENAME ===
# Better than pathlib.rename() for cross-device moves
shutil.move('old_location/file.txt', 'new_location/file.txt')

# === DELETE DIRECTORIES ===
# Delete entire directory tree (even if not empty)
shutil.rmtree('folder_with_contents')  # CAREFUL! No confirmation

# Safer delete (check what you're deleting)
def on_error(func, path, exc_info):
    print(f"Error deleting {path}: {exc_info[1]}")

shutil.rmtree('folder', onerror=on_error)

# === ARCHIVE/COMPRESS ===
# Create archive
shutil.make_archive('backup', 'zip', 'folder_to_compress')
shutil.make_archive('backup', 'tar', 'folder_to_compress')
shutil.make_archive('backup', 'gztar', 'folder_to_compress')  # .tar.gz

# Unpack archive
shutil.unpack_archive('backup.zip', 'extract_here')
shutil.unpack_archive('backup.tar.gz', 'extract_here')

# === DISK USAGE ===
total, used, free = shutil.disk_usage('/')  # In bytes
print(f"Free: {free / 1e9:.1f} GB")

# === GET TERMINAL SIZE ===
columns, lines = shutil.get_terminal_size()
print(f"Terminal: {columns}x{lines}")