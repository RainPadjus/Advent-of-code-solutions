with open('data5.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]


instr= []
for i in data:
    if "move" in i:
        instr.append(i)

print("######")
i = 0
stack = []
buf = []
while i<=len(data) and data[i]!="":
    stack.append(data[i].replace("    ", "x").replace("[","").replace("]", "").replace(" ", "").replace("x", " "))
    i+=1

#stack.pop(-1)
print(stack)
#stack[level][column][]

stacks = []
buf = []
for j in range(len(stack)):
    for i in stack:
        buf.append(i[j])
    stacks.append(buf)
    buf = []

print("*****")
#stacks = stacks[]
for i in range(len(stacks)):
    stacks[i] = stacks[i][::-1]


for i in stacks:
    while " " in i:
        i.pop()


for i in stacks:
    print(i)
#parser for commands
m = []
for inst in instr:
    i = inst.split()
    for t in range(int(i[1])):
        stacks[int(i[5])-1].append(stacks[int(i[3])-1].pop())
    for t in range(int(i[1])):
        m.append(stacks[int(i[5])-1].pop())
    m = m[::-1] 
    for t in range(int(i[1])):
        stacks[int(i[5])-1].append(m.pop())

f = ""
for s in stacks:
        f+=s.pop()

print(f)
print(m)