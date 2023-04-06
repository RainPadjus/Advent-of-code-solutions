with open('data8.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]

grid = []
buf = []
for i in data:
    for j in i:
        buf.append(int(j))
    grid.append(buf)
    buf = []

#for i in grid: print(i)

c=0
right = []
flag=True
scores = []
for i in range(len(grid)):
    for j in range(len(grid)):
        flag=True
        if (i<1)or (j<1) or (i==len(grid)-1) or (j==len(grid)-1):
            c+=1
        else:
            #print("FOR: ", i,"-",j)
            right = []
            r = 1
            while flag:
                try:
                    right.append(grid[i][j+r])
                    r+=1
                except:
                    #print("right: ",right)
                    flag=False

            flag=True
            left = []
            l = 1
            while flag:
                if (j-l)>=0:
                    left.append(grid[i][j-l])
                    l+=1
                else:  
                    #print("left: ",left)
                    flag=False
            
            flag=True
            up = []
            u = 1
            while flag:
                if (i-u)>=0:
                    up.append(grid[i-u][j])
                    u+=1
                else:  
                    #print("up: ",up)
                    flag=False


            flag=True
            down = []
            d = 1
            while flag:
                try:
                    down.append(grid[i+d][j])
                    d+=1
                except:
                    #print("down: ",down)
                    flag=False

            #if grid[i][j]>max(down) or grid[i][j]>max(up) or grid[i][j]>max(left) or grid[i][j]>max(right):
            #    c+=1
            score = 0
            dd=0
            dda = True
            uu=0
            uua = True
            ll=0
            lla = True
            rr=0
            rra = True

            for d in down:
                if d<grid[i][j] and dda:
                    dd+=1
                else:
                    if dda: dd+=1
                    dda = False

            for u in up:
                if u<grid[i][j] and uua: 
                    uu+=1
                else: 
                    if uua: uu+=1
                    uua = False

            for l in left:
                if l<grid[i][j] and lla: 
                    ll+=1
                else:
                    if lla: ll+=1
                    lla = False

            for r in right:
                if r<grid[i][j] and rra: 
                    rr+=1
                else:
                    if rra: rr+=1 
                    rra = False

            #print("DD: ", dd)
            #print("UU: ", uu)
            #print("LL: ", ll)
            #print("RR: ", rr)
            score=dd*uu*ll*rr
            #print("SCORE" , score)
            scores.append(score)
            #print("down: ",down)
            #print("up: ",up)
            #print("left: ",left)
            #print("right: ",right)

print(c)
print(max(scores))