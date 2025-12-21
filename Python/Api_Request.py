import requests

response=requests.get("https://api.github.com/users/mishrp13/repos")




#print(response.json())
#print(type(response.json()))
#print(response.json()[0])

my_project=response.json()

for project in my_project:
    print(f"Project Name: {project['name']}\nProject Url: {project['url']}\n ")