from pathlib import Path

# === CREATE PATHS (Doesn't create actual files yet) ===
p = Path('folder/subfolder/file.txt')
p = Path.home() / 'Documents' / 'project' / 'data.csv'  # Nice path joining!

# === CREATE FILES & FOLDERS ===
# Create directory (with parents)
p.parent.mkdir(parents=True, exist_ok=True)  # Creates folder/subfolder

# Create empty file
p.touch()  # Creates file.txt
p.touch(exist_ok=True)  # Won't error if exists

# === CHECK PROPERTIES ===
p.exists()      # Does it exist?
p.is_file()     # Is it a file?
p.is_dir()      # Is it a directory?
p.stat().st_size  # File size in bytes
p.stat().st_mtime  # Last modified timestamp

# === LIST & SEARCH ===
# List contents
for item in Path('.').iterdir():
    print(item.name)

# Find all Python files recursively
py_files = list(Path('.').rglob('*.py'))

# Find files matching pattern
txt_files = list(Path('.').glob('*.txt'))

# === READ/WRITE ===
# Write text
p.write_text('Hello World', encoding='utf-8')

# Read text
content = p.read_text(encoding='utf-8')

# Write bytes
p.write_bytes(b'binary data')

# === RENAME/MOVE (within same filesystem) ===
original = Path('old.txt')
new_name = Path('new.txt')
original.rename(new_name)  # Rename/move file

# === DELETE ===
p.unlink()  # Delete file
# Note: Can't delete non-empty directories with pathlib