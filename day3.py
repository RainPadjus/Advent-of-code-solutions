with open('data3.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]

print(data)

acc = 0
i = 0
while i<=len(data)-3:

    z = set(data[i]).intersection(set(data[i+1])).intersection(set(data[i+2]))
    print(z)
    if str(z)[2] == (str(z)[2]).lower():
        acc += ord(str(z)[2])-96
    else:
        acc += ord(str(z)[2])-65+27

    i+=3

print(acc)