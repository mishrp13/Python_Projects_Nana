# set does not allow duplicate values

calculation_to_units=24
name_of_unit="hours"

def days_to_unit(number_of_days):
    return f"{number_of_days} days are {number_of_days*calculation_to_units} {name_of_unit}"

def validate_and_execute():
    try:
        user_input_number=int(num_of_days_element)
        if user_input_number>0:
            calculated_value=days_to_unit(user_input_number)
            print(calculated_value)
        elif user_input_number==0:
            print("You entered 0, please enter the valid number ")
        else:
            print("You enter negative, please enter valid number")
    except ValueError:
        print("your input is not valid, please don't ruin my program")

user_input=""
while user_input!="exit":
    user_input=input("Enter the number of days, so that we can convert it into hours \n")
    list_of_days=user_input.split(", ")
    print(list_of_days)
    print(set(list_of_days))

    print(type(list_of_days))
    print(type(set(list_of_days)))


    for num_of_days_element in set(list_of_days):
        validate_and_execute()

        

   