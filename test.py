def sum_(lis):
    total=0
    s = 0
    l = len(lis) - 1
    while(s<=l):
        if s==l:
            total += lis[s]
            s += 1
        else:
            total += lis[s] + lis[l]
            l -= 1
            s += 1
    return total

def sum_f(lis):
    total = 0
    for i in lis:
        total += i
    return total

lis = range(10000) 
import time

start = time.time()
print sum_f(lis)
end = time.time()
print(end - start)
start = time.time()
print sum_(lis) 
end = time.time()
print(end - start)
