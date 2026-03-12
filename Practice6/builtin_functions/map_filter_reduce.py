from functools import reduce

numbers = [1,2,3,4,5,6,7,8,9,10]

def square_number(x):
    return x ** 2
def is_even(x):
    return x % 2 == 0
def add_numbers(a, b):
    return a + b
def multiply_numbers(a, b):
    return a * b
def sort_descending(x):
    return -x

squared_numbers = list(map(square_number, numbers))
print(squared_numbers)

even_numbers = list(filter(is_even, numbers))
print(even_numbers)

total_sum = reduce(add_numbers, numbers)
print(total_sum)

product = reduce(multiply_numbers, numbers)
print(product)

sorted_numbers = sorted(numbers, key=sort_descending)
print(sorted_numbers)


# other built-in functions
print(len(numbers))
print(sum(numbers))
print(min(numbers))
print(max(numbers))