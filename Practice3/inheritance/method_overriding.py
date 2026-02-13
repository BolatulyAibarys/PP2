#Overriding — это когда в дочернем(child) классе мы пишем метод с тем же именем, что и в родительском(parent), 
# и он заменяет(replaces) родительский метод.

class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof")

#причина в том, что родительский init больше не вызывается автоматически.
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self):
        print("Dog created")

d = Dog()  #works

print(d.name) #error because Animal.init не был вызван