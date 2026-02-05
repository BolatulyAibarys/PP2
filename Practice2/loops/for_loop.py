#With the for loop we can execute a set of statements, once for each item in a list, tuple, set etc.
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

#Even strings are iterable objects, they contain a sequence of characters:
for x in "banana":
  print(x)

#The range() function returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), 
#and ends at a specified number.
for x in range(2, 30, 3):
  print(x)

#The else keyword in a for loop specifies a block of code to be executed when the loop is finished:
#The else block will NOT be executed if the loop is stopped by a break statement.
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")

#The "inner loop" will be executed one time for each iteration of the "outer loop":
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)

#for loop with no content, put in the pass statement to avoid getting an error.
for x in [0, 1, 2]:
  pass