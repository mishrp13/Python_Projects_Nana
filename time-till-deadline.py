import datetime

user_input = input("enter your goal with deadline separated by colon:\n")
user_list=user_input.split(":")

goal=user_list[0]
deadline=user_list[1]

deadline_date=datetime.datetime.strptime(deadline,"%d.%m.%Y")
today_date=datetime.datetime.today()

#calculate how many days left for from now till deadline

time_till=deadline_date-today_date
print(f"Dear user time remaining for the goal: {goal} is {time_till.days} days")
