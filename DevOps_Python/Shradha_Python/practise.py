import re
phone_number_pattern_object=re.compile(r'\d{3}-\d{3}-\d{4}')
match_obj=phone_number_pattern_object.search("my number is 123-456-0974")
print(match_obj.group())