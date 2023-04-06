with open('data4.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]
count = 0
flag = True
for i in data: 
    d = i.split(",")
    print(d)
    for parts in d:
        f = parts.split("-")
        one = set([])
        i = int(f[0])    
        while i <= int(f[1]):
            one.add(i)
            i+=1
        if flag:
            sec = one.copy()
            flag = False

    if len(set.intersection(one, sec)) > 0:
        count +=1
    flag= True

print(count)