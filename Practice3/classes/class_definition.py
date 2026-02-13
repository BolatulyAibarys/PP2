#A class defines what an object should look like, and an object is created based on that class. For example:
"""
Class	    Objects
Fruit   	Apple, Banana, Mango
Car     	Volvo, Audi, Toyota
"""

#To create a class, use the keyword class:
#Create a class named MyClass, with a property named x:
#Create an objects named p, and print the value of x:
class MyClass:
  x = 5

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)

#You can delete objects by using the del keyword:
del p1