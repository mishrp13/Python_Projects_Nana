logs = ["unique","error","info","info"]
unique = []

for item in logs:
    if item not in unique:
        unique.append(item)

print(unique)
