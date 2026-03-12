names = ["Ali","Aruzhan","Dana"]
scores = [85,90,78]

# enumerate()
for index, name in enumerate(names, start=1):
    print(index, name)

# zip()
for name, score in zip(names, scores):
    print(name, score)