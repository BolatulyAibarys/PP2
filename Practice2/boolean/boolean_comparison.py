#Any string is True, except empty strings.
#Any number is True, except 0.
#Any list, tuple, set, and dictionary are True, except empty ones
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#empty values, such as (), [], {}, "", the number 0, and the value None, value False evaluates to False.
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})