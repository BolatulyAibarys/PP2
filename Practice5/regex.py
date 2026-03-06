import re

s = input("Enter a string: ")

#1 Match string that has 'a' followed by zero or more 'b'
pattern = r'ab*'
result = re.findall(pattern, s)
print("1:", result)


#2 Match string that has 'a' followed by two to three 'b'
pattern = r'ab{2,3}'
result = re.findall(pattern, s)
print("2:", result)


#3 Find sequences of lowercase letters joined with underscore
pattern = r'[a-z]+_[a-z]+'
result = re.findall(pattern, s)
print("3:", result)


#4 Find sequences of one uppercase letter followed by lowercase letters
pattern = r'[A-Z][a-z]+'
result = re.findall(pattern, s)
print("4:", result)


#5 Match string that has 'a' followed by anything, ending in 'b'
pattern = r'a.*b'
result = re.findall(pattern, s)
print("5:", result)


#6 Replace space, comma, or dot with colon
result = re.sub(r'[ ,.]', ':', s)
print("6:", result)


#7 Convert snake_case to camelCase
def snake_to_camel(text):
    parts = text.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

print("7:", snake_to_camel(s))


#8 Split string at uppercase letters
result = re.findall(r'[A-Z][^A-Z]*', s)
print("8:", result)


#9 Insert spaces between words starting with capital letters
result = re.sub(r'(?<!^)(?=[A-Z])', ' ', s)
print("9:", result)


#10 Convert camelCase to snake_case
result = re.sub(r'([A-Z])', r'_\1', s).lower()
print("10:", result)