class Student:
    school = "KBTU"   # class variable
    count = 0         # class variable

    def __init__(self, name):
        self.name = name   # instance variable
        Student.count += 1


s1 = Student("Ali")
s2 = Student("Dana")

print(Student.school)
print(Student.count)




class Dog:
    species = "Canine"

d1 = Dog()
d2 = Dog()

Dog.species = "Animal"

print(d1.species)
print(d2.species)




class Person:
    type = "Human"   # class variable

    def __init__(self, name):
        self.name = name   # instance variable


p1 = Person("Aruzhan")
p2 = Person("Nurlan")

print(p1.type)
print(p2.type)
print(p1.name)