with open('data1.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]
data.append("")

acc= 0 
buf = []

for i in data:
    if i == "":
        buf.append(acc)
        acc=0
    else:
        acc+=int(i)

print(max(buf))
print(sum(sorted(buf)[-3:]))