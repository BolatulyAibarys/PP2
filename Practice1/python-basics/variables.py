#1 type
x = 5
y = "John"
print(type(x))
print(type(y))

#2 many val to many var
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#3 unpacking a collection
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

#4 local var
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

#5 global var
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)