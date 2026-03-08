import os

# === CHECK EXISTENCE & TYPE ===
os.path.exists('file.txt')        # True if exists
os.path.isfile('file.txt')        # True if file
os.path.isdir('folder/')          # True if directory
os.path.islink('link')            # True if symbolic link

# === CREATE/REMOVE ===
os.mkdir('new_dir')                        # Create single directory
os.makedirs('a/b/c', exist_ok=True)        # Create nested directories
os.remove('file.txt')                       # Remove file
os.rmdir('empty_dir')                       # Remove empty directory

# === LIST DIRECTORY ===
files = os.listdir('.')                     # List all items
files = [f for f in os.listdir('.')         # List only files
         if os.path.isfile(f)]

# === WALK DIRECTORY TREE ===
for root, dirs, files in os.walk('.'):
    # root: current directory
    # dirs: subdirectories in root
    # files: files in root
    for file in files:
        full_path = os.path.join(root, file)
        print(full_path)

# === GET FILE INFO ===
stats = os.stat('file.txt')
size = stats.st_size                    # File size in bytes
mtime = stats.st_mtime                  # Last modified timestamp
atime = stats.st_atime                  # Last accessed timestamp
ctime = stats.st_ctime                  # Creation timestamp (Unix: metadata change)





import os

# === PATH JOINING ===
path = os.path.join('folder', 'subfolder', 'file.txt')
# Result: 'folder/subfolder/file.txt' (OS-specific separators)

# === PATH SPLITTING ===
dir_name, file_name = os.path.split('/path/to/file.txt')
# dir_name = '/path/to', file_name = 'file.txt'

base, ext = os.path.splitext('file.txt')
# base = 'file', ext = '.txt'

# === ABSOLUTE PATHS ===
abs_path = os.path.abspath('relative/path')
real_path = os.path.realpath('link.txt')  # Resolves symlinks

# === COMMON PATHS ===
home = os.path.expanduser('~')           # User home: /home/user or C:\Users\user
cwd = os.getcwd()                        # Current working directory
os.chdir('/new/path')                    # Change directory



import os

# === ENVIRONMENT VARIABLES ===
value = os.environ.get('PATH')           # Get environment variable
os.environ['MY_VAR'] = 'value'           # Set variable (current process only)
home = os.environ.get('HOME') or os.environ.get('USERPROFILE')

# === SYSTEM COMMANDS ===
exit_code = os.system('ls -la')          # Run shell command
# Returns exit code (0 usually means success)

# === PROCESS INFO ===
pid = os.getpid()                        # Current process ID
ppid = os.getppid()                      # Parent process ID
os.getuid()                              # User ID (Unix)
os.getgid()                              # Group ID (Unix)

# === SYSTEM INFO ===
os.name                                  # 'posix', 'nt', 'java'
os.sep                                   # Path separator: '/' or '\\'
os.pathsep                               # PATH separator: ':' or ';'
os.linesep                               # Line separator: '\n' or '\r\n'



import os

def find_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                py_files.append(full_path)
    return py_files

# Alternative with list comprehension
py_files = [os.path.join(root, f)
            for root, dirs, files in os.walk('.')
            for f in files if f.endswith('.py')]