import re
pattern= re.compile(r"[a-zA-Z0-9]")
cool=pattern.findall("Robocop eats A  Baby food")
print(cool)

