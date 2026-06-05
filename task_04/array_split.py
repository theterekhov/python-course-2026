n = int(input())
a = list(map(int, input().split()))

total = sum(a)

if total != 0:
    print("YES")
    print(1)
    print(1, n)
else:
    prefix = 0
    found = False
    for i in range(n):
        prefix += a[i]
        if prefix != 0:
            print("YES")
            print(2)
            print(1, i + 1)
            print(i + 2, n)
            found = True
            break
    
    if not found:
        print("NO")
