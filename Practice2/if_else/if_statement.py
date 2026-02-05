#An "if statement" is written by using the if keyword.
a = 33
b = 200
if b > a:
  print("b is greater than a")

#If the condition is true, the code block inside the if statement is executed. If the condition is false, the code block is skipped.
number = 15
if number > 0:
  print("The number is positive")

#Boolean variables can be used directly in if statements without comparison operators.
is_logged_in = True
if is_logged_in:
  print("Welcome back!")

#if statement with no content, put in the pass statement to avoid getting an error.
age = 16

if age < 18:
  pass #Add underage logic later
else:
  print("Access granted")