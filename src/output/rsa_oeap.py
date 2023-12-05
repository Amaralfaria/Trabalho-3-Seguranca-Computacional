import math
import hashlib
import os
from rsa import criptografar_rsa, descriptografar_rsa


def sha1(mensagem_em_bytes):
    """Retorna o hash SHA-1 da mensagem."""
    return hashlib.sha1(mensagem_em_bytes).digest()


def i2osp(x, xlen):
    """Converte um inteiro para uma sequência de bytes (big-endian)."""
    return x.to_bytes(xlen, 'big')


def os2ip(x):
    """Converte uma sequência de bytes para um inteiro."""
    return int.from_bytes(x, 'big')


def mgf1(seed, mlen):
    """Geração de máscara usando a função de hash SHA-1."""
    hlen = len(sha1(b''))
    return b''.join(sha1(seed + i2osp(c, 4)) for c in range(0, math.ceil(mlen / hlen)))[:mlen]


def xor(dado, mascara):
    """Realiza a operação XOR entre duas sequências de bytes."""
    return bytes((d ^ m) for d, m in zip(dado, mascara))


def oaep_encode(mensagem_em_bytes, k, rotulo=b''):
    db = sha1(rotulo) + b'\x00' * (k - len(mensagem_em_bytes) - 2 * len(sha1(rotulo)) - 2) + b'\x01' + mensagem_em_bytes
    seed = os.urandom(len(sha1(rotulo)))
    db_mask = mgf1(seed, k - len(sha1(rotulo)) - 1)
    masked_db = xor(db, db_mask)
    seed_mask = mgf1(masked_db, len(sha1(rotulo)))
    masked_seed = xor(seed, seed_mask)
    return b'\x00' + masked_seed + masked_db


def oaep_decode(texto_cifrado, k, rotulo=b''):
    masked_seed, masked_db = texto_cifrado[1:1 + len(sha1(rotulo))], texto_cifrado[1 + len(sha1(rotulo)):]
    seed_mask = mgf1(masked_db, len(sha1(rotulo)))
    seed = xor(masked_seed, seed_mask)
    db_mask = mgf1(seed, k - len(sha1(rotulo)) - 1)
    db = xor(masked_db, db_mask)
    for i in range(len(sha1(rotulo)), len(db)):
        if db[i] == 0:
            continue
        elif db[i] == 1:
            break

    return db[i + 1:]


def cifrar_oaep(mensagem_em_bytes, chave_publica):
    """Cifra uma mensagem usando OAEP e a chave pública RSA."""
    n, _ = chave_publica
    k = (n.bit_length() + 7) // 8
    return i2osp(criptografar_rsa(os2ip(oaep_encode(mensagem_em_bytes, k)), chave_publica), k)


def decifrar_oaep(texto_cifrado, chave_privada):
    """Decifra uma mensagem cifrada usando OAEP e a chave privada RSA."""
    n, _ = chave_privada
    k = (n.bit_length() + 7) // 8
    return oaep_decode(i2osp(descriptografar_rsa(os2ip(texto_cifrado), chave_privada), k), k)
