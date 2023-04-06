with open('data7.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]

tree = {"/" : {}}
file_size =  {}
cur = []
def command(x):
    if x == "cd /":
        cur.append("/")
    elif x == "cd ..":
        cur.pop()
    elif "cd " in x:
        cur.append(x[3:])

for i in data:
    #print(tree)
    if i[0] == "$":
        command(i[2:])
    elif i.split()[0] == "dir":
        code = "tree"
        for c in cur:
            code+="['"
            code+=c
            code+="']"
        code += '= {i.split()[1]: ""}'
        exec(code)
    else:
        if str(cur) in file_size.keys():
               file_size[str(cur)] += int(i.split()[0])
        else:
            file_size[str(cur)] = int(i.split()[0])

        #print(i.split()[0])
#print(tree)
#print(file_size)
ii = 0
jj = 0
for i in file_size.keys():
    for j in file_size.keys():
        if i == j:
            pass
        else:
            #print(i, " - ", j)
            if i.replace("[", "").replace("]", "").replace("'", "").replace(",", "") in j.replace("[", "").replace("]", "").replace("'", "").replace(",", ""):
                file_size[i] += file_size[j]


        jj+=1
    jj = 0
    ii += 1

s = 0
for k in file_size.keys():
    if file_size[k] <= 100000:
        s+=file_size[k]

#print(tree)
#print(file_size)
print(s)