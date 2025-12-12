calculation_to_unit=24
name_of_unit="hours"

def days_to_units(number_of_days):
    if number_of_days > 0:
        return f"{number_of_days} days are {calculation_to_unit*number_of_days} {name_of_unit}"
    elif number_of_days==0:
        return f" you entered 0, please enter valid positive number "
    else:
        return "you enter the wrong value"

my_input=input("enter the value so that we convert it into hours \n")

if my_input.isdigit():
    user_input=int(my_input)
    calculated_value=days_to_units(my_input)
    print(calculated_value)
else:
    print("please enter valid number")


