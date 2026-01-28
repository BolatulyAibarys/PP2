#1 multiline string
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

#2 printing letters of string
a = "Hello, World!"
print(a[1:3])
print(len(a))

#3 string looping
for x in "banana":
  print(x)

#4 checking for word in string
txt = "The best things in life are free!"
print("free" in txt)
if "free" in txt: # use ("word" not in txt) if checking for errors
  print("Yes, 'free' is present.")

#5 operations
a = "    Hello, World!   "
print(a.upper())
print(a.lower())
print(a.strip()) # returns "Hello, World!"

#6 replacing letters(words) and splitting
a = "Hello, World!"
print(a.replace("H", "J"))
print(a.split(",")) # returns ['Hello', ' World!']

#7 f-strings
age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)

txt = f"The price is {20 * 59} dollars"
print(txt)

#8 escape characters
txt = "We are the so-called \"Vikings\" from the north."