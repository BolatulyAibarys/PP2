#Arguments are specified after the function name, inside the parentheses. You can add as many arguments as you want, just separate them with a comma.
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

#A parameter is the variable listed inside the parentheses in the function definition.
#An argument is the actual value that is sent to the function when it is called.
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument

#You can assign default values to parameters. If the function is called without an argument, it uses the default value:
def my_function(country = "Norway"):
  print("I am from", country)

my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")

#This way, with keyword arguments, the order of the arguments does not matter.
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(name = "Buddy", animal = "dog")

#You can send any data type as an argument to a function (string, number, list, dictionary, etc.).
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)



def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)

#Arguments before / are positional-only, and arguments after * are keyword-only:
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)