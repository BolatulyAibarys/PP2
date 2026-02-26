#deg to rad
import math

degree = float(input("Input degree: "))
radian = math.radians(degree)  # функция math.radians делает перевод
print(f"Output radian: {radian:.6f}")


#area of trapezoid
# Формула: S = (a + b) / 2 * h
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = (base1 + base2) / 2 * height
print(f"Expected Output: {area}")


#area of regular poligon
import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

# Формула: (n * s^2) / (4 * tan(pi/n))
area = (n * s**2) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {area}")


#area of a parallelogram
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height
print(f"Expected Output: {area}")