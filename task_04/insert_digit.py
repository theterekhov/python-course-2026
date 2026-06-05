t = int(input())

for _ in range(t):
    n, d = map(int, input().split())
    num = input().strip()
    
    pos = n
    for i in range(n):
        if int(num[i]) < d:
            pos = i
            break
    
    print(num[:pos] + str(d) + num[pos:])
