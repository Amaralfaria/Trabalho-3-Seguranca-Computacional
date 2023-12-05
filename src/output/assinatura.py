import base64
from hashlib import sha3_256
from rsa import criptografar_rsa, descriptografar_rsa


def codificar_base64(assinatura):
    try:
        return base64.b64encode(assinatura).decode("ascii")
    except Exception as e:
        print("Não foi possível codificar base64", e)
        return


def decodificar_base64(assinatura):
    try:
        return base64.b64decode(assinatura)
    except Exception as e:
        print("Não foi possível decodificar base64", e)
        return


def assinar(plaintext, chave_publica):
    try:
        hashed = sha3_256(plaintext.encode('utf-8')).digest()
        signature = criptografar_rsa(int.from_bytes(hashed, "big"), chave_publica)
        signature_bytes = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
        return codificar_base64(signature_bytes)
    except Exception as e:
        print("Não foi possível assinar", e)
        return


def verificar_assinatura(assinatura, plaintext, chave_privada):
    try:
        assinatura_bytes = decodificar_base64(assinatura)
        hash_plaintext = sha3_256(plaintext).digest()
        assinatura_em_inteiro = int.from_bytes(assinatura_bytes, "big")
        
        # Descriptografa a assinatura usando RSA e verifica a igualdade com o hash original
        if descriptografar_rsa(assinatura_em_inteiro, chave_privada) == int.from_bytes(hash_plaintext, "big"):
            print("Assinatura válida com sucesso!")
        else:
            print("Assinatura inválida!")
    except Exception as e:
        print("Erro ao verificar assinatura:", e)