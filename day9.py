with open('data9.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]

tail_pointer  = [0,0]
head_pointer = [0,0]
tail_hist = []


def dist(x,y):
    d = 1

    for z,zz in zip(x,y):
        if abs(z-zz)<2:
            d*=True
        else:
            d*=False
    return (not d)

for i in data:
    if i.split()[0] == 'R':
        for time in range(int(i.split()[1])):
            if tail_pointer not in tail_hist:
                tail_hist.append(tail_pointer)
            print("R")
            prev = head_pointer.copy()
            head_pointer[0] += 1
            if(dist(head_pointer, tail_pointer)):
                tail_pointer = prev
            
            print("H", head_pointer)
            print("T", tail_pointer)

    if i.split()[0] == 'L':
        for time in range(int(i.split()[1])):
            if tail_pointer not in tail_hist:
                tail_hist.append(tail_pointer)
            print("L")
            prev = head_pointer.copy()
            head_pointer[0] -= 1
            if(dist(head_pointer, tail_pointer)):
                tail_pointer = prev
            print("H", head_pointer)
            print("T", tail_pointer)

    if i.split()[0] == 'U':
        for time in range(int(i.split()[1])):
            if tail_pointer not in tail_hist:
                tail_hist.append(tail_pointer)
            print("U")
            prev = head_pointer.copy()
            head_pointer[1] += 1
            if(dist(head_pointer, tail_pointer)):
                tail_pointer = prev
            print("H", head_pointer)
            print("T", tail_pointer)

    if i.split()[0] == 'D':
        for time in range(int(i.split()[1])):
            if tail_pointer not in tail_hist:
                tail_hist.append(tail_pointer)
            print("D")
            prev = head_pointer.copy()
            head_pointer[1] -= 1
            if(dist(head_pointer, tail_pointer)):
                tail_pointer = prev    

print(len(tail_hist))