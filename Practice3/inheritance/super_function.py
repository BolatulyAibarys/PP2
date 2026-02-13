#super() function that will make the child class inherit all the methods and properties from its parent:
#super().__init__(name)     means вызови __init__ родительского класса
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name):
        super().init(name)
        print("Dog created")

d = Dog("Bob")
print(d.name)  #now it works




class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

x = Student("Mike", "Olsen", 2024)
x.welcome()