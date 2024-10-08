def leap_year(year):
    return (year % 4 ==0 and year % 100 != 0) or year % 400 != 0

def days_in_feb(year):
    return 29 if year is leap_year else 28

year = int(input("Enter the year you want to check:"))

if leap_year(year):
    print(f"{year} is a leap year")
else:
    print(f"{year} is  not a leap year")

print(f"Feb of {year} has {days_in_feb(year)}")
