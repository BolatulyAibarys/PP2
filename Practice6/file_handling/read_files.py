# #1 Read and print file examples

with open("sample.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# readline()
with open("sample.txt", "r", encoding="utf-8") as file:
    print(file.readline(), end="")
    print(file.readline(), end="")

# readlines()
with open("sample.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())