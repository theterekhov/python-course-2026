t = int(input())

for _ in range(t):
    n = int(input())
    digits = list(map(int, input().split()))
    
    min_digit = min(digits)
    idx = digits.index(min_digit)
    digits[idx] += 1
    
    product = 1
    for d in digits:
        product *= d
    
    print(product)
