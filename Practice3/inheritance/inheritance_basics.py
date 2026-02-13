#Parent class is the class being inherited from, also called base class.

#Child class is the class that inherits from another class, also called derived class.
#Use the Person class to create an object, and then execute the printname method:
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

x = Person("John", "Doe")
x.printname()



class Student(Person):
  pass

x = Student("Mike", "Olsen")
x.printname()