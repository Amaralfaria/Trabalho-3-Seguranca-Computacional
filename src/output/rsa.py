import random as rd
import math
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
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

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

def areCoprime(n1,n2):
    return math.gcd(n1,n2) == 1

def rsaKeys(prime1, prime2):
    n_coprime = (prime1-1)*(prime2-1)
    prime_product = prime1*prime2
    public_key = ()
    private_key = ()
    e = 0
    d = 0

    for i in range(2,n_coprime):
        if areCoprime(i,prime_product) and areCoprime(i,n_coprime):
            e = i
            break
    
    mod_number = pow(e, -1, n_coprime)

    # print(mod_number, e, n_coprime)
    # print('resto')
    # print((e*mod_number)%n_coprime)

    public_key = (e,prime_product)
    private_key = (mod_number, prime_product)

    return (public_key,private_key)

def rsaOperation(number, key):
    return pow(number,key[0],key[1])

def stringToNumber(s):
    number = ''
    for c in s:
        number += str(ord(c))

    return int(number)



n_bits = 1024
p1 = generatePrime(n_bits)
p2 = generatePrime(n_bits)
# p1 = 53
# p2 = 41

msg = 'ola mundo'
number = stringToNumber(msg)
print(number)
# print(p1)
# print()
# print(p2)

public_key, private_key = rsaKeys(p1,p2)
ciphered = rsaOperation(number,public_key)
deciphered = rsaOperation(ciphered,private_key)


print(ciphered)
print()
print(deciphered)


# print(mod_number, e, n_coprime)

# for i in range(20):
#     print('numero:', 11*i, 'resto por 24:',(11*i)%24)














