#In Python, a function is defined using the def keyword, followed by a function name and parentheses:
def my_function():
  print("Hello from a function")

my_function()
my_function()
my_function()

#With functions, you write the code once and reuse it:
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#Functions can send data back to the code that called them using the return statement.
#When a function reaches a return statement, it stops executing and sends the result back:
def get_greeting():
  return "Hello from a function"

print(get_greeting())

#Function definitions cannot be empty. If you need to create a function placeholder without any code, use the pass statement:
def my_function():
  pass