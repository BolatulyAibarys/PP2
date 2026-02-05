#The else statement is executed when the if condition (and any elif conditions) evaluate to False.
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

#The else statement provides a default action when none of the previous conditions are true.
number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")

#You can combine if, elif, and else to create a comprehensive decision-making structure.
temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")

#The else statement acts as a fallback that executes when none of the preceding conditions are true.
username = "Emil"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")