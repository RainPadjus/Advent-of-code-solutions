with open('data2.txt') as f:
    lines = f.readlines()
data = [x.replace("\n", "") for x in lines]

#print(data)

#A for Rock, B for Paper, and C for Scissors
#X for Rock, Y for Paper, and Z for Scissors

#shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
#(0 if you lost, 3 if the round was a draw, and 6 if you won).
#X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win

score = 0
for i in data:
    #outcome:
    
    if i[0] == "A":
        if i[2] == "X":
            score+=3
        elif i[2] == "Y":
            score+=1
            score+=3
        else:
            score+=2
            score+=6
    if i[0] == "B":
        if i[2] == "X":
            score+=1
        elif i[2] == "Y":
            score+=3
            score+=2
        else:
            score+=6
            score+=3
    if i[0] == "C":
        if i[2] == "X":
            score+=2
        elif i[2] == "Y":
            score+=3
            score+=3
        else:
            score+=1
            score+=6

print(score)