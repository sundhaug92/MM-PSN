import sys

def factorial(n):
    r = 1
    for i in range(1, n + 1):
        r *= i
    return r

def binomial_coefficient(n, k):
    if k > n or k < 0:
        return 0
    return factorial(n) / (factorial(k) * factorial(n - k))

def binomial_distribution(n, k):
    if k > n or k < 0:
        return 0
    return binomial_coefficient(n, k) / (2 ** n)

def main():
    known_bits = sys.argv[1]
    model(known_bits)

def model(known_bits):
    length = 24+len(known_bits) -1 # 
    missing = 64 - length
    if missing < 0:
        print("Error: known_bits length exceeds 64 bits.")
        return
    zeros = known_bits.count('0')
    ones = known_bits.count('1')
    print('LE', length)
    print('MI', missing)
    print('Z0', zeros)
    print('O1', ones)
    
    ones_to_add = 0
    for i in range(missing + 1):
        ones_to_add = i
        zeros_to_add = missing - i
        if ones_to_add + ones > zeros_to_add + zeros:
            break
    
    # print(f'Adding {ones_to_add} in {missing}')
    chance = sum([binomial_distribution(missing, _) for _ in range(ones_to_add, missing + 1)])
    print(f'Chance of {ones_to_add} ones in {missing} bits: {100*chance:.2f}')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python model.py <known_bits>")
        sys.exit(1)
    main()
