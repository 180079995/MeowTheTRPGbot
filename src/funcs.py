import random

def rolldice(num,side):
    nums=[]
    for i in range(num):
        nums.append(random.randint(1,side))
    return nums

def getdicepoint(num,side):
    return sum(rolldice(num,side))