import random as rd
import math
import hashlib
import os



def millerRabin(n, number_of_rounds=15):
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


def encrypt_rsa(message, public_key):
    n, e = public_key
    return pow(message, e, n)

def decrypt_rsa(ciphertext, private_key):
    n, d = private_key
    return pow(ciphertext, d, n)


def stringToNumber(s):
    number = ''
    for c in s:
        number += str(ord(c))

    return int(number)

def sha1(b_message):
    return hashlib.sha1(b_message).digest()

def i2osp(x, xlen):
    return x.to_bytes(xlen, 'big')

def os2ip(x):
    return int.from_bytes(x, 'big')

def mgf1(seed, mlen):
    hlen = len(sha1(b''))
    return b''.join(sha1(seed + i2osp(c, 4)) for c in range(0, math.ceil(mlen / hlen)))[:mlen]

def xor(data, mask):
    return bytes((d ^ m) for d, m in zip(data, mask))

def oaep_encode(b_message, k, label=b''):
    db = sha1(label) + b'\x00' * (k - len(b_message) - 2 * len(sha1(label)) - 2) + b'\x01' + b_message
    seed = os.urandom(len(sha1(label)))
    db_mask = mgf1(seed, k - len(sha1(label)) - 1)
    masked_db = xor(db, db_mask)
    seed_mask = mgf1(masked_db, len(sha1(label)))
    masked_seed = xor(seed, seed_mask)
    return b'\x00' + masked_seed + masked_db

def oaep_decode(ciphertext, k, label=b''):
    masked_seed, masked_db = ciphertext[1:1 + len(sha1(label))], ciphertext[1 + len(sha1(label)):]
    seed_mask = mgf1(masked_db, len(sha1(label)))
    seed = xor(masked_seed, seed_mask)
    db_mask = mgf1(seed, k - len(sha1(label)) - 1)
    db = xor(masked_db, db_mask)
    for i in range(len(sha1(label)), len(db)):
        if db[i] == 0:
            continue
        elif db[i] == 1:
            break

    return db[i + 1:]

def encrypt_oaep(b_message, public_key):
    n, _ = public_key
    k = (n.bit_length() + 7) // 8
    return i2osp(encrypt_rsa(os2ip(oaep_encode(b_message, k)), public_key), k)

def decrypt_oaep(ciphertext, private_key):
    n, _ = private_key
    k = (n.bit_length() + 7) // 8
    return oaep_decode(i2osp(decrypt_rsa(os2ip(ciphertext), private_key), k), k)

if __name__ == "__main__":
    n_bits = 1024
    p1 = generatePrime(n_bits)
    p2 = generatePrime(n_bits)
    print(f"Length of the primes generated: {len(str(p1))}, {len(str(p2))}\n")
    public_key, private_key = rsaKeys(p1, p2)
    message = "Localização do tesouro XY"
    byte_message = message.encode('utf-8')
    print(b_message)
    ciphertext = encrypt_oaep(byte_message, public_key)
    print(ciphertext)
    plaintext = decrypt_oaep(ciphertext, private_key)
    print(plaintext.decode('utf-8', errors='replace'))














