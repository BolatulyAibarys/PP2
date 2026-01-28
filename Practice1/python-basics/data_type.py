#1 floats
x = 35e3
y = 12E4
z = -87.7e100

print(type(x))
print(type(y))
print(type(z))

#2 complexes
x = 3+5j
y = 5j
z = -5j

print(type(x))
print(type(y))
print(type(z))

#3 random num generation
import random

print(random.randrange(1, 10))

#4 casting to f
x = float(1)     # x will be 1.0
y = float(2.8)   # y will be 2.8
z = float("3")   # z will be 3.0
w = float("4.2") # w will be 4.2

#5 casting to int
x = int(1)   # x will be 1
y = int(2.8) # y will be 2
z = int("3") # z will be 3