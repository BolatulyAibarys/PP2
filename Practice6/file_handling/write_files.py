# #1 Create a text file and write sample data

with open("sample.txt", "w", encoding="utf-8") as file:
    file.write("Line 1: Hello\n")
    file.write("Line 2: Python file handling\n")
    file.write("Line 3: Practice example\n")

# #2 Append new lines

with open("sample.txt", "a", encoding="utf-8") as file:
    file.write("Line 4: Appended text\n")
    file.write("Line 5: Another appended line\n")

# file mode x example

try:
    with open("only_once.txt", "x", encoding="utf-8") as file:
        file.write("Created using x mode\n")
except FileExistsError:
    pass