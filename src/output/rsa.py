import random as rd
"""
def getM(number):
    if number%2 == 1:
        return -1
    
    exponent = 1
    m = 0
    
    while number%(2**exponent) == 0:
        exponent+=1
    
    exponent-=1
    m = int(number/(2**exponent))

    return m

def millerRabin(candidate):
    previousNumber = candidate - 1
    m = getM(previousNumber)

    a = rd.randint(2,previousNumber-1)
   
     
    bi = (a**m)%candidate
    

    while bi not in (1,-1):
        bi = (bi**2)%candidate

    if bi == -1:
        return True
    return False
"""


def millerRabin(n, k=5):
    """
    Miller-Rabin primality test.
    
    Parameters:
    - n: The number to be tested for primality.
    - k: The number of iterations for the test. Higher values of k provide greater confidence.
    
    Returns:
    - True if n is likely a prime, False if it is definitely composite.
    """
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as 2^r * d + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = rd.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Definitely composite

    return True  # Likely prime


def generatePrime(n_bits):
    prime_candidate = rd.getrandbits(n_bits)
    while not millerRabin(prime_candidate):
        prime_candidate = rd.getrandbits(n_bits)

    return prime_candidate

print(generatePrime(1024))










