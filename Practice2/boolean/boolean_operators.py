#You can create functions that returns a Boolean Value:
def myFunction() :
  return True

print(myFunction())

#You can execute code based on the Boolean answer of a function:
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

#Python also has many built-in functions that return a boolean value, like the isinstance() function,
#which can be used to determine if an object is of a certain data type:
x = 200
print(isinstance(x, int))