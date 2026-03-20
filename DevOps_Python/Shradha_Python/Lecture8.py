# class Student:
#     name = "Karan"

# s1= Student()
# print(s1.name)


#--------------------------

# class Car:
#     color= "blue"
#     name= "mercedes"

# car1 =Car()
# print(car1.color)
# print(car1.name)

#--------------------------------

# class Student:

#     College_name= "chandigarh University"
#     name = "annonymous" # class attr
#     #default contructor
#     def __int__(self):
#         pass

#     #parameterized contructor
#     def __init__(self,fullname,marks):
#         self.name=fullname # obj attr > class attr
#         self.marks=marks
#         print("adding a new student in database")


# s1= Student("Karan",97)
# print(s1.name,s1.marks)

# s2= Student("Arjun",33)
# print(s2.name,s2.marks)

# print(s2.College_name)
# print(Student.College_name)

#----------------------------------

# class Student:

#     def __init__(self,name,marks):
#         self.name=name 
#         self.marks=marks
    
#     #Methods = functions inside class
#     def welcome(self):
#         print("welcome", self.name)
#     #Methods
#     def get_marks(self):
#         return self.marks
    

# s1=Student("karan",33)
# s1.welcome()
# print(s1.get_marks())

#--------------------------------------------

# class Student:

#     def __init__(self,name,marks):
#         self.name=name
#         self.marks=marks

#     @staticmethod
#     def hello():
#         print("Hello")

#     def get_avg(self):
#         sum=0
#         for val in self.marks:
#             sum += val
#         print(f"Hi , {self.name} your avergae score is {sum/3}")



# s1 = Student("Karan", [23,33,49])
# s1.get_avg()

# s1.name= "Tony"
# s1.get_avg()

#------------------------------------------------

# #Abstraction
# #hiding information
# class Car:

#     def __init__(self):
#         self.acc= False
#         self.brk= False
#         self.clutch= False

#     def start(self):
#         self.acc= True
#         self.brk= True
#         print("car started...")

# car1= Car()
# car1.start()

# # Encapsulation is wrapping data and function into a single unit
# # Till now what we did was encapsulation and abstraction

#------------------------------------------------------

class Account:

    def __init__(self,bal,acc):
        self.balance=bal
        self.account=acc

    def debit(self,ammount):
        self.balance -= ammount
        print(f"Rs {ammount} is debited")
        print(f"Total balance is : {self.get_balance()}")

    def credit(self,ammount):
        self.balance += ammount
        print(f"Rs {ammount} is credited")
        print(f"Total balance is : {self.get_balance()}")
    
    def get_balance(self):
        return self.balance


acc1 = Account(100000,12345)
acc1.debit(5000)
acc1.credit(96)



