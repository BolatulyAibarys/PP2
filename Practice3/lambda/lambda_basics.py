#lambda arguments : expression    it returns the result
x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

#The power of lambda is better shown when you use them as an anonymous function inside another function.
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

#use the same function definition to make both functions, in the same program:
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))