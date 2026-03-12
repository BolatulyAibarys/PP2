import os
import shutil

# #1 Copy file
shutil.copy("sample.txt", "sample_copy.txt")

# #2 Backup file
shutil.copy("sample.txt", "sample_backup.txt")

# #3 Delete file safely
file_to_delete = "sample_copy.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)