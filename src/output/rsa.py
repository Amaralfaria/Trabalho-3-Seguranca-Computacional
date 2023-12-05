import random as rd
import math


def millerRabin(n, numero_de_rounds=40):
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

    for _ in range(numero_de_rounds):
        a = rd.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False 

    return True  # Provavelmente primo

def gerarPrimo(n_bits):
    candidato_primo = rd.getrandbits(n_bits)
    while not millerRabin(candidato_primo):
        candidato_primo = rd.getrandbits(n_bits)

    return candidato_primo



def chavesRSA(primo1, primo2):
    n = primo1 * primo2
    e = 65537 # Valor utilizado para segurança e compatibilidade
    phi = (primo1 - 1) * (primo2 - 1)
    d = pow(e, -1, phi)
    chave_publica = (n, e)
    chave_privada = (n, d)
    return (chave_publica, chave_privada)

def criptografar_rsa(mensagem, chave_publica):
    n, e = chave_publica
    return pow(mensagem, e, n)

def descriptografar_rsa(ciphertext, chave_privada):
    n, d = chave_privada
    return pow(ciphertext, d, n)
















