# Python File System Modules Guide

## 📁 `pathlib` - Use For:
- **Path manipulation and building**
- **File creation/checking**
- **Reading/writing small files**
- **Pattern matching with glob**
- **Working with file extensions/stems**

### Key Features:
- Object-oriented path handling
- Platform-independent path operations
- Clean syntax with `/` operator for path joining
- Built-in glob pattern matching
- Convenient file read/write methods

### Example:
```python
from pathlib import Path

# Path joining
config_path = Path.home() / '.config' / 'app' / 'settings.json'

# Create directory and file
config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.touch()

# Read/write
config_path.write_text('{"theme": "dark"}')
content = config_path.read_text()

# Pattern matching
py_files = list(Path('.').glob('*.py'))
```

---

## 🔄 `shutil` - Use For:
- **Copying/moving files**
- **Backup operations**
- **Cleaning up directories**
- **Creating/extracting archives**
- **Cross-filesystem operations**

### Key Features:
- High-level file operations
- Recursive directory operations
- Archive creation/extraction
- Cross-device file moving
- Disk usage information

### Example:
```python
import shutil
from pathlib import Path

# Copy files with metadata
shutil.copy2('source.txt', 'dest.txt')

# Copy entire directory
shutil.copytree('source_dir', 'dest_dir', dirs_exist_ok=True)

# Create archive
shutil.make_archive('backup', 'zip', 'data_folder')

# Remove directory tree
shutil.rmtree('temp_folder')
```

---

## ⚙️ `os` - Use For:
- **System-level operations**
- **Environment variables**
- **Process management**
- **File permissions**
- **Directory walking**
- **Platform-specific code**

### Key Features:
- Low-level operating system interfaces
- Process and environment management
- File descriptor operations
- Platform detection
- Permission handling

### Example:
```python
import os
import stat

# Environment variables
home_dir = os.environ.get('HOME')

# Directory walking
for root, dirs, files in os.walk('.'):
    for file in files:
        full_path = os.path.join(root, file)
        print(full_path)

# File permissions
os.chmod('script.sh', stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)

# System commands
os.system('echo "Hello from shell"')
```

---

## 📊 Quick Decision Guide:

| Task | Recommended Module |
|------|-------------------|
| Creating/joining paths | `pathlib` |
| Checking if file exists | `pathlib` |
| Reading/writing text files | `pathlib` |
| Pattern matching files | `pathlib` |
| Copying files/directories | `shutil` |
| Moving files (cross-device) | `shutil` |
| Creating archives | `shutil` |
| Deleting directory trees | `shutil` |
| Environment variables | `os` |
| Process management | `os` |
| File permissions | `os` |
| Recursive directory walking | `os.walk()` |

---

## 🔗 Best Practices:

1. **Use `pathlib` as your default choice** for path-related operations
2. **Combine modules effectively**:
   ```python
   from pathlib import Path
   import shutil
   
   # Good pattern: pathlib for paths, shutil for operations
   source = Path('data/input.csv')
   dest = Path('backups') / source.name
   shutil.copy2(source, dest)
   ```

3. **Use `os` only when necessary** for system-level operations

4. **Remember platform differences** - `pathlib` handles these automatically

5. **Always handle exceptions** when performing file operations

---

## 🎯 Summary:

- **`pathlib`**: Your daily driver for path manipulation and basic file ops
- **`shutil`**: Your power tool for advanced file operations and archiving
- **`os`**: Your specialized toolkit for system-level tasks and platform-specific code

Choose based on your specific need, and don't hesitate to combine them for optimal solutions!