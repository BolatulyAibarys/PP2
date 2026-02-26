#squares of int up to n
def squares_up_to(N):
    for i in range(N+1):
        yield i*i

N = int(input())
for sq in squares_up_to(N):
    print(sq)


#print odd int from 0 to n, devided with comma
n = int(input())

def evens(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i

print(",".join(str(x) for x in evens(n)))


#int devisible to 3, 4 from 0 to n
def divisible_by_3_and_4(n):
    for i in range(n+1):
        if i % 12 == 0:  # кратные и 3 и 4
            yield i

n = int(input())
print(" ".join(str(x) for x in divisible_by_3_and_4(n)))


#squares of int from a to b
def squares(a, b):
    for i in range(a, b+1):
        yield i*i

a, b = map(int, input().split())
for val in squares(a, b):
    print(val)


#numbers from n to 0
def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input())
for val in countdown(n):
    print(val)