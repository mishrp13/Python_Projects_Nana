calculation_to_units=24
name_of_unit="hours"

def days_to_unit(number_of_days):
    if number_of_days >0:
        return f"{number_of_days} days are {number_of_days*calculation_to_units} {name_of_unit}"
    elif number_of_days==0:
        return f"you entered 0, please enter valid number"
    
def validate_and_execute():
    if user_input.isdigit():
        user_input_number=int(user_input)
        calculated_value=days_to_unit(user_input_number)
        print(calculated_value)
    else:
        print("Please enter valid number")



user_input=input("Hey enter the days so that i can convert it into hours \n")
validate_and_execute()