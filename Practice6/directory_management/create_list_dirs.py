import os
from pathlib import Path

# #1 Create nested directories
nested_path = os.path.join("project_folder", "main", "subfolder")
os.makedirs(nested_path, exist_ok=True)

# #2 List files and folders
for item in os.listdir("."):
    print(item)

# #3 Find files by extension

# find .txt files
for item in os.listdir("."):
    full_path = os.path.join(".", item)
    if os.path.isfile(full_path) and item.endswith(".txt"):
        print(item)

# find .py files using pathlib
for file in Path(".").glob("*.py"):
    print(file.name)

# extra directory functions
print(os.getcwd())