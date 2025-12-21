class User:
    def __init__(self,user_email,name,password,current_job_title):
        self.email=user_email
        self.name = name
        self.password=password
        self.current_job_title= current_job_title

    
    def change_password(self,new_password):
        self.password=new_password
    
    def change_job_title(self,new_job_title):
        self.current_job_title=new_job_title

    def get_user_info(self):
        print(f" User {self.name} currently works as {self.current_job_title}. you can contact them at {self.email}")


app_user_one=User("prabalsonu1997@gmail.com", "Prabal" ,"123@qwe", "DevOps Engineer" )
app_user_one.get_user_info()

app_user_one.change_job_title("DevOps Trainer")
app_user_one.get_user_info()

app_user_two= User("Rajvansh@gmail.com", "Raj", "234@gmail.com", "Agent")
app_user_two.get_user_info()