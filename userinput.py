calculation_to_units= 24
name_of_unit= "hours"

def days_to_unit(num_of_days):
    return f"{num_of_days} days are {num_of_days*calculation_to_units} {name_of_unit}"

user_input=int(input("Hey user, enter the number of days so that i convert it into hours \n"))
result=days_to_unit(user_input)
print(result)