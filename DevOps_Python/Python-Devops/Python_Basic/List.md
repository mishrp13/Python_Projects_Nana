✅ 1. Filter Servers by Role
servers = ["web1", "db1", "web2", "cache1"]
web_servers = [s for s in servers if "web" in s]
print(web_servers)

👉 Output: ['web1', 'web2']
💡 Uses list comprehension + filtering

✅ 2. Count ERROR Logs
logs = ["INFO", "ERROR", "WARNING", "ERROR", "INFO"]
error_count = logs.count("ERROR")
print(error_count)

👉 Output: 2
💡 Built-in method (very clean)

✅ 3. Remove Duplicate IPs
ips = ["10.0.0.1", "10.0.0.2", "10.0.0.1"]
unique_ips = list(set(ips))
print(unique_ips)

👉 Output: ['10.0.0.1', '10.0.0.2']
⚠️ Order not preserved

✅ 4. List → Dictionary
servers = ["web1", "web2", "web3"]
server_dict = {s: "active" for s in servers}
print(server_dict)

👉 Output:

{'web1': 'active', 'web2': 'active', 'web3': 'active'}
✅ 5. Flatten Nested List
data = [["pod1", "pod2"], ["pod3", "pod4"]]
flat = [item for sublist in data for item in sublist]
print(flat)

👉 Output: ['pod1', 'pod2', 'pod3', 'pod4']

✅ 6. Common Elements
list1 = ["web1", "web2", "db1"]
list2 = ["web2", "db1", "cache1"]
common = list(set(list1) & set(list2))
print(common)

👉 Output: ['web2', 'db1']

✅ 7. Remove Duplicates (Keep Order)
logs = ["INFO", "ERROR", "INFO", "WARNING"]
unique = []
for item in logs:
    if item not in unique:
        unique.append(item)
print(unique)

👉 Output: ['INFO', 'ERROR', 'WARNING']
💡 Interview favorite!

✅ 8. Split Servers
servers = ["web1", "db1", "web2", "db2"]

web = [s for s in servers if "web" in s]
db = [s for s in servers if "db" in s]

print(web)
print(db)
✅ 9. Max / Min CPU
cpu = [20, 50, 10, 80]

print(max(cpu))  # 80
print(min(cpu))  # 10
✅ 10. Rotate List
nums = [1, 2, 3, 4, 5]
k = 2

rotated = nums[-k:] + nums[:-k]
print(rotated)

👉 Output: [4, 5, 1, 2, 3]

⭐ BONUS: Second Largest
nums = [10, 20, 4, 45, 99]

nums = list(set(nums))   # remove duplicates
nums.sort()
print(nums[-2])

👉 Output: 45

-------------------------------------

🔥 1. Find Missing Servers
servers_expected = ["web1", "web2", "web3"]
servers_running = ["web1", "web3"]

✅ Task: Find missing servers

missing = [s for s in servers_expected if s not in servers_running]
print(missing)

👉 Output: ['web2']
💡 Logic: Compare expected vs actual

🔥 2. Merge Two Lists Without Duplicates
list1 = ["web1", "web2"]
list2 = ["web2", "db1"]
merged = list(set(list1 + list2))
print(merged)

👉 Output: ['web1', 'web2', 'db1']
💡 Logic: Combine → remove duplicates using set

🔥 3. Find Index of All Occurrences
logs = ["ERROR", "INFO", "ERROR", "WARNING"]
indexes = [i for i, v in enumerate(logs) if v == "ERROR"]
print(indexes)

for i, v in enumerate(logs):
    if v == "error":
        indexes.append(i)

print(indexes)

👉 Output: [0, 2]
💡 Logic: Use enumerate() to track index

🔥 4. Group Elements by Condition
nums = [1, 2, 3, 4, 5, 6]
even = [x for x in nums if x % 2 == 0]
odd = [x for x in nums if x % 2 != 0]

👉 Output: even [2,4,6], odd [1,3,5]
💡 Logic: Conditional filtering

🔥 5. Find First Non-Repeating Element
data = [1, 2, 2, 3, 3, 4]
for x in data:
    if data.count(x) == 1:
        print(x)
        break

👉 Output: 1
💡 Logic: Count frequency

🔥 6. Chunk a List (VERY USEFUL)
nums = [1,2,3,4,5,6,7,8]
n = 3
chunks = [nums[i:i+n] for i in range(0, len(nums), n)]
print(chunks)

👉 Output: [[1,2,3],[4,5,6],[7,8]]
💡 DevOps use: batch processing 
 nums[0:0+3] → nums[0:3] → [1,2,3]

 chunks = []
for i in range(0, len(nums), n):
    chunks.append(nums[i:i+n])

🔥 7. Reverse Without Built-in
nums = [1, 2, 3, 4]
rev = []
for x in nums:
    rev = [x] + rev
print(rev)

👉 Output: [4,3,2,1]
💡 Logic: prepend elements

🔥 8. Check if List is Palindrome
nums = [1, 2, 3, 2, 1]
if nums == nums[::-1]:
    print("Palindrome")

👉 Output: Palindrome
💡 Logic: Compare with reverse

🔥 9. Find All Pairs with Given Sum
nums = [1, 2, 3, 4, 5]
target = 6
pairs = []
for i in range(len(nums)):
    for j in range(i+1, len(nums)):
        if nums[i] + nums[j] == target:
            pairs.append((nums[i], nums[j]))
print(pairs)

👉 Output: [(1,5), (2,4)]
💡 Logic: Nested loop comparison

🔥 10. Running Sum (Prefix Sum)
nums = [1, 2, 3, 4]
result = []
total = 0
for x in nums:
    total += x
    result.append(total)

print(result)

👉 Output: [1,3,6,10]
💡 DevOps use: cumulative metrics

🔥 11. Find Majority Element
nums = [1,1,2,1,3,1,1]
for x in nums:
    if nums.count(x) > len(nums)//2:
        print(x)
        break

👉 Output: 1

🔥 12. Remove All Occurrences of Element
nums = [1,2,3,2,4]
result = [x for x in nums if x != 2]
print(result)

👉 Output: [1,3,4]