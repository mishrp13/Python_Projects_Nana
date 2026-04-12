def count_up_to(limit):
    """Generates numbers from 1 up to (and including) the limit.

    Args:
        limit (int): The upper limit for counting.

    Returns:
        generator(int): The generator to lazily count up to limit.
    """
    print("Generator function started...")
    n = 1

    while n <= limit:
        print(f"Yielding {n}")
        yield n
        print(f"Resumed after yielding {n}.")
        n += 1

    print("Generator function finished.")


count_gen = count_up_to(2)

# print("first call to next outside of for loop")
# print(next(count_gen))

# print("second call to next outside of for loop")
# print(next(count_gen))

# print("remaining from inside loop")
# for num in count_gen:
#     print(num)

print(next(count_gen))
print(next(count_gen))

try:
    print(next(count_gen))
except StopIteration:
    print("generator finished")


for number in count_gen:
    print(number)