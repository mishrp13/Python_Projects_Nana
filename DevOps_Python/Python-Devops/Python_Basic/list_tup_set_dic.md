🟢 SECTION 1: LISTS (1–30)
Basics
Create a list of 5 server names
Access the 3rd element
Add a new server
Remove a server
Find length of list
Intermediate
Iterate over list
Filter only “web” servers
Convert all names to uppercase
Reverse a list
Sort a list
Advanced
Remove duplicates
Find second largest number
Flatten nested list
Rotate list by k steps
Find common elements between 2 lists
DevOps-style
Find missing servers
Count ERROR logs
Group servers by type
Find index of all matches
Split list into chunks
Logic building
Find max/min
Sum all elements
Multiply all elements
Check if element exists
Remove all occurrences
Challenging
Find pairs with given sum
First non-repeating element
Running sum
Check palindrome
Merge lists without duplicates
🟡 SECTION 2: TUPLES (31–45)
Basics
Create a tuple
Access elements
Slice a tuple
Convert tuple to list
Convert list to tuple
Intermediate
Count occurrences
Find index of element
Loop through tuple
Tuple unpacking
Swap variables using tuple
Advanced
Nested tuple access
Use tuple as dictionary key
Compare tuples
Return multiple values from function
Immutable behavior demo
🔵 SECTION 3: SETS (46–70)
Basics
Create a set
Add elements
Remove elements
Check membership
Remove duplicates from list
Intermediate
Union of two sets
Intersection
Difference
Symmetric difference
Convert list to set
Advanced
Find common servers
Find unique logs
Check subset
Check superset
Remove duplicates preserving logic
DevOps-style
Compare two environments
Find missing configs
Unique IP addresses
Detect drift between systems
Fast lookup scenario
Challenging
Find elements present in only one list
Remove common elements
Merge sets
Count unique values
Set comprehension
🟣 SECTION 4: DICTIONARIES (71–100)
Basics
Create dictionary
Access value
Add new key
Delete key
Get all keys
Intermediate
Get all values
Loop through dict
Use .items()
Use .get() safely
Merge two dictionaries
Advanced
Count frequency of elements
Invert dictionary
Sort dictionary by key
Sort by value
Nested dictionary access
DevOps-style
Store server config
Parse JSON response
Count log types
Group data by key
Build config map
Challenging
Find key with max value
Remove duplicate values
Merge multiple dicts
Default values handling
Dictionary comprehension
Real-world logic
Track server status
Map IP → hostname
Count API responses
Build environment config
Combine list + dict + set logic


# 1–5 Basic
servers = ["web1","web2","db1","cache1","web3"]
print(servers[2])
servers.append("web4")
servers.remove("db1")
print(len(servers))

# 6–10
for s in servers: print(s)
web = [s for s in servers if "web" in s]
upper = [s.upper() for s in servers]
rev = servers[::-1]
servers.sort()

# 11–15
unique = list(set(servers))
nums = [10,20,5,30]
nums.sort(); print(nums[-2])
nested = [[1,2],[3,4]]
flat = [x for sub in nested for x in sub]
k=2; rotated = nums[-k:]+nums[:-k]
common = list(set(["a","b"]) & set(["b","c"]))

# 16–20
expected=["web1","web2"]; running=["web1"]
missing=[s for s in expected if s not in running]
logs=["ERROR","INFO","ERROR"]; print(logs.count("ERROR"))
group={"web":[],"db":[]}
for s in servers:
    if "web" in s: group["web"].append(s)
idx=[i for i,v in enumerate(logs) if v=="ERROR"]
chunks=[servers[i:i+2] for i in range(0,len(servers),2)]

# 21–25
nums=[1,2,3]
print(max(nums),min(nums))
print(sum(nums))
prod=1
for n in nums: prod*=n
print("web1" in servers)
filtered=[x for x in nums if x!=2]

# 26–30
nums=[1,2,3,4,5]; target=5
pairs=[(a,b) for i,a in enumerate(nums) for b in nums[i+1:] if a+b==target]
data=[1,2,2,3]
print(next(x for x in data if data.count(x)==1))
running=[]; total=0
for x in nums: total+=x; running.append(total)
print(nums==nums[::-1])
merged=list(set([1,2]+[2,3]))


t=(1,2,3,2)

# basics
print(t[1])
print(t[1:3])
l=list(t)
t2=tuple(l)

# intermediate
print(t.count(2))
print(t.index(3))
for x in t: print(x)
a,b,c,_=t
x,y=1,2
x,y=y,x

# advanced
nested=((1,2),(3,4))
print(nested[1][0])
d={(1,2):"point"}
print((1,2)<(2,3))
def fun(): return 1,2
a,b=fun()

# immutable demo
# t[0]=10 ❌ (error)

s={1,2,3}

# basics
s.add(4)
s.remove(2)
print(1 in s)
unique=list(set([1,1,2]))

# intermediate
a={1,2,3}; b={2,3,4}
print(a|b)   # union
print(a&b)   # intersection
print(a-b)   # difference
print(a^b)   # symmetric

# advanced
print(set(["web1","web2"]) & set(["web2"]))
print(set(["ERROR","INFO"]))
print({1,2}.issubset({1,2,3}))
print({1,2,3}.issuperset({2}))
ordered_unique=list(dict.fromkeys([1,2,2,3]))

# DevOps
env1={"web","db"}; env2={"web"}
print(env1-env2)
ips=set(["1.1.1.1","1.1.1.1"])
drift=env1^env2

# challenging
only_one=list(set(a)^set(b))
no_common=list(set(a)-set(b))
merged=a|b
print(len(set([1,2,2,3])))
sq={x*x for x in range(5)}


d={"a":1,"b":2}

# basics
print(d["a"])
d["c"]=3
del d["b"]
print(d.keys())

# intermediate
print(d.values())
for k,v in d.items(): print(k,v)
print(d.get("x","default"))
d2={"d":4}
merged={**d,**d2}

# advanced
data=["a","b","a"]
freq={}
for x in data:
    freq[x]=freq.get(x,0)+1

inv={v:k for k,v in d.items()}
print(dict(sorted(d.items())))
print(dict(sorted(d.items(), key=lambda x:x[1])))

nested={"env":{"prod":3}}
print(nested["env"]["prod"])

# DevOps
config={"env":"prod","replicas":3}
import json
json_data='{"a":1}'
parsed=json.loads(json_data)

logs=["ERROR","INFO","ERROR"]
count={l:logs.count(l) for l in set(logs)}

group={}
for x in ["web1","web2"]:
    group.setdefault("web",[]).append(x)

# challenging
print(max(d,key=d.get))
unique_vals=set(d.values())
multi={**d,**d2}
default=d.get("missing",0)
comp={x:x*x for x in range(5)}

# real-world
servers={"web1":"up","web2":"down"}
ip_map={"1.1.1.1":"web1"}
api=["200","500","200"]
resp_count={r:api.count(r) for r in set(api)}
env={"prod":{"web":3}}

# combine
servers=["web1","web2"]
status={s:"up" for s in servers}
unique=set(servers)



