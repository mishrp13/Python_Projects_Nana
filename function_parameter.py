calculation_to_units=24
name_of_units="hour"

def days_to_unit(number_of_days,custom_mesage):
    print(f"{number_of_days} days are {number_of_days*calculation_to_units} {name_of_units}")
    print(custom_mesage)

# days_to_unit(45,"Awesome")
# days_to_unit(35,"Looks good")
# days_to_unit(65,"yes")

def scope_check(number_of_days):
    my_var="Variable inside function"
    print(number_of_days)
    print(name_of_units)
    print(my_var)


scope_check(30)

#start from 1 hour