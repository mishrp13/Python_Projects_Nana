calculation_to_units=24
name_of_units="hours"

def days_to_units(number_of_days):
    return f"{number_of_days} days are {number_of_days*calculation_to_units} {name_of_units}"

my_var=days_to_units(20)
print(my_var)