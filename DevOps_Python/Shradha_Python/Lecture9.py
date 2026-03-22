#del

# class Student:

#     def __init__(self,name):
#         self.name=name

# s1= Student("Prabal")
# print(s1.name)
# del s1.name
# print(s1.name)

#------------------------------

# class Account:
#     def __init__(self,acc_no,acc_pass):
#         self.acc_no=acc_no
#         self.__acc_pass=acc_pass # private

#     def reset_pass(self):
#         print(self.__acc_pass) # This will run beacause it is inside class

# acc1= Account("12345","abcde")
# print(acc1.acc_no)
# #print(acc1.__acc_pass) # This will fail beacuse it is outside class
# print(acc1.reset_pass())


#---------------------------------------------

# class Person:

#     __name= "anonymous"

#     def __hello(self):
#         print("hello person!")

#     def welcome(self):
#         self.__hello()

# p1 =Person()
# print(p1.welcome())

#---------------------------------------------
# Inheritence

# single level inheritence
# class Car:
#     color= "Black"
#     @staticmethod
#     def start():
#         print("car started..")
    
#     @staticmethod
#     def stop():
#         print("car stopped..")

# class ToyotaCar(Car):
#     def __init__(self,name):
#         self.name=name

# car1=ToyotaCar("fortuner")
# car2=ToyotaCar("pirus")

# print(car1.name)
# print(car1.start())
# print(car1.color)

#----------------------------------------------------

# Multilevel

# class Car:
    
#     @staticmethod
#     def start():
#         print("car started...")

#     @staticmethod
#     def stop():
#         print("car stopped..")

# class ToyotaCar(Car):
#     def __init__(self,brand):
#         self.brand=brand

# class Fortuner(ToyotaCar):
#     def __init(self,type):
#         self.type=type

# car1= Fortuner("diesel")
# print(car1.start())

#-----------------------------------------

# Multiple inheritence

# class A:
#     VarA = "welcome to class A"

# class B:
#     VarB = "welcome to class B"

# class C(A,B):
#     VarC = "welcome to class C"

# c1 = C()
# print(c1.VarA)
# print(c1.VarB)
# print(c1.VarC)

#-------------------------------------
# super()

# class Car:

#     def __init__(self,type):
#         self.type=type

#     @staticmethod
#     def start():
#         print("car started..")

#     @staticmethod
#     def stop():
#         print("car stopped..")

# class ToyotaCar(Car):
#     def __init__(self,name,type):
#         super().__init__(type)
#         self.name=name
#         super().start()


# car1 = ToyotaCar("Pirus","electric")
# print(car1.type)

#----------------------------------------
#class Attribute


# class person:
#     name= "annonymous"

#     def changeName(self,name):
#         self.name=name

# p1 = person()
# p1.changeName("Rahul")
# print(p1.name)
# print(person.name)

# in the above case name is not getting changed in class Attribute
# instead it is getting changed in the differnt object

# class Person:
#     name = "annonymous"

#     def changeName(self,name):
#         Person.name=name

# p1= Person()
# p1.changeName("Rahul")
# print(p1.name)
# print(Person.name)

# now in this above case class attribute name will change

# class Person:
#     name = "annonymous"

#     def changeName(self,name):
#         self.__class__.name = "Rahul"

# p1= Person()
# p1.changeName("Rahul")
# print(p1.name)
# print(Person.name)

#-------------------------------------------------------
# Now if we want within the function itself we can access our class directly 
# then we can do using class method

# class Person:
#     name= "annonymous"
    
#     @classmethod
#     def changeName(cls,name):
#         cls.name=name

# p1=Person()
# p1.changeName("Rahul")
# print(p1.name)
# print(Person.name)

# # so there are three methods
# # 1. static Methods
# # 2. class Methods (cls)
# # 3. instance Methods (self)


#----------------------------------------------------

#This is one of the way to change perectage of student and not hardcoding
# the value instead calling a function to change the perecntage as well
# class Student:

#     def __init__(self,phy,chem,math):
#         self.phy=phy
#         self.chem=chem
#         self.math=math
#         self.percentage=str((self.phy + self.chem + self.math)/3) + "%"

#     def calPercentage(self):
#         self.percentage=str((self.phy + self.chem + self.math)/3) + "%"



# stu1=Student(33,37,38)
# print(stu1.percentage)
# stu1.phy=97
# print(stu1.phy)
# stu1.calPercentage()
# print(stu1.percentage)

# # Now simplest way to do above code by the property attribute

# class Student:
#     def __init__(self,phy,chem,math):
#         self.phy=phy
#         self.chem=chem
#         self.math=math

#     @property
#     def percentage(self):
#         return str((self.phy + self.math + self.chem)/3) + "%"
    

# stu1=Student(97,98,99)
# print(stu1.percentage)
# stu1.math=33
# print(stu1.percentage)

#---------------------------------------------------------

# polymorphism
# operator overloading


# class Complex:
    
#     def __init__(self,real,img):
#         self.real=real
#         self.img=img
    
    
     
#     def showNumber(self):
#         print(self.real,"i +", self.img, "j")
    
#     def __add__(self,num8):  # dunder function
#         newReal= self.real + num8.real
#         newImg= self.img + num8.img
#         return Complex(newReal,newImg)
    
#     def __sub__(self,num8):  # dunder function
#         newReal= self.real - num8.real
#         newImg= self.img - num8.img
#         return Complex(newReal,newImg)
    

# num1 = Complex(1,3)
# num1.showNumber()


# num2 = Complex(4,6)
# num2.showNumber()


# num3= num1 + num2
# num3.showNumber()


# num3= num1 - num2
# num3.showNumber()

# # num3 = num1.add(num2)
# # num3.showNumber()

#---------------------------------------------------

# class Circle:

#     def __init__(self,radius):
#         self.radius=radius

#     def area(self):
#         return (22/7) * self.radius**2
    
#     def perimeter(self):
#         return 2 * (22/7) * self.radius
    

# c1 = Circle(21)
# print(c1.area())
# print(c1.perimeter())

#------------------------------------------------------

# class Employee:

#     def __init__(self,role,dept,salary):
#         self.role=role
#         self.dept=dept
#         self.salary=salary

#     def showDetails(self):
#         print("role =",self.role)
#         print("dept =",self.dept)
#         print("salary =",self.salary)


# class Engineer(Employee):
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age
#         super().__init__("Engineer","IT","75,000")


# engg1= Engineer("Elon musk",40)
# engg1.showDetails()


#-----------------------------------------------

class Order:

    def __init__(self,item,price):
        self.item=item
        self.price=price

    def __gt__(self,ord2):
        return self.price > ord2.price
    
ord1= Order("chips",20)
ord2= Order("Mango",56)
print(ord1 > ord2)













