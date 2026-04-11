def filter_evens(data):
    print(f"filter evens starting")

    for item in data:
        if item%2 == 0:
            print(f"filter_evens: yielding {item}")
            yield item

    print(f"filter_evens: finished")

evens_from_range= filter_evens(range(6))
print(f"Generator object created: {evens_from_range}")

for num in evens_from_range:
    print(f"Recieved even: {num}")

evens_from_list = filter_evens([0,1,2,3,4,5,6])

print(f"generator object created : {evens_from_list}")

for num in evens_from_list:
    print(f"Recieved even: {num}")
