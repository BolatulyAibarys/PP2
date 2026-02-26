#subtract 5 days from now
from datetime import datetime, timedelta

today = datetime.now()
new_date = today - timedelta(days=5)
print(new_date)


#yesterday, today, tomorrow
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


#remove microseconds from datetime
from datetime import datetime

now = datetime.now()
without_microseconds = now.replace(microsecond=0)
print(without_microseconds)


#difference bet 2 date in seconds
from datetime import datetime

dt1 = datetime.strptime(input("Enter first datetime (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")
dt2 = datetime.strptime(input("Enter second datetime (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")

delta = abs(dt2 - dt1)  #timedelta между датами
seconds = delta.total_seconds() #переводит timedelta в секунды
print(int(seconds))