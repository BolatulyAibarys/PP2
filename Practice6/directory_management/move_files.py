import os
import shutil

# #4 Move/copy files between directories

source_dir = "source_dir"
destination_dir = "destination_dir"

os.makedirs(source_dir, exist_ok=True)
os.makedirs(destination_dir, exist_ok=True)

source_file = os.path.join(source_dir, "example.txt")
copy_file = os.path.join(destination_dir, "example_copy.txt")
moved_file = os.path.join(destination_dir, "example_moved.txt")

with open(source_file, "w", encoding="utf-8") as file:
    file.write("Example file\n")

shutil.copy(source_file, copy_file)
shutil.move(source_file, moved_file)

# extra directory management functions
single_folder = "single_folder"

if not os.path.exists(single_folder):
    os.mkdir(single_folder)

print(os.getcwd())

os.chdir(single_folder)
print(os.getcwd())

os.chdir("..")

if os.path.exists(single_folder) and len(os.listdir(single_folder)) == 0:
    os.rmdir(single_folder)

if os.path.exists(source_dir) and len(os.listdir(source_dir)) == 0:
    os.rmdir(source_dir)