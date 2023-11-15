import random as rd
import math



def millerRabin(n, number_of_rounds=40):
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

    for _ in range(number_of_rounds):
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

    for i in range(2,n_coprime):
        if areCoprime(i,prime_product) and areCoprime(i,n_coprime):
            e = i
            break
    
    mod_number = pow(e, -1, n_coprime)
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





if __name__ == "__main__":
    n_bits = 1024
    p1 = generatePrime(n_bits)
    p2 = generatePrime(n_bits)
    print(f"Length of the primes generated: {len(str(p1))}, {len(str(p2))}\n")

    plaintext = "Localização do tesouro nas coordenadas X E Y"
    print(f"Plaintext:\n {plaintext}")
    number = stringToNumber(plaintext)
    print(f"Message in number format:\n{number}")

    public_key, private_key = rsaKeys(p1,p2)
    cipher = rsaOperation(number,public_key)
    decipher = rsaOperation(cipher,private_key)


    print(f"Text ciphered: \n{cipher}")
    print()
    print(f"Text deciphered:\n {decipher}")













