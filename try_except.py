calculation_to_units=24
name_of_unit="hours"

def days_to_unit(number_of_days):
    return f"{number_of_days} days are {number_of_days*calculation_to_units} {name_of_unit}"

def validate_and_execute():
    try:
        user_input_number=int(user_input)
        if user_input_number>0:
            calculated_value=days_to_unit(user_input_number)
            print(calculated_value)
        elif user_input_number==0:
            print("You entered 0, please enter the valid number ")
        else:
            print("You enter negative, please enter valid number")
    except ValueError:
        print("your input is not valid, please don't ruin my program")



user_input=input("Enter the number of days, so that we can convert it into hours \n")
validate_and_execute()