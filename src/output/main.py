from rsa import chavesRSA, gerarPrimo
from assinatura import assinar, verificar_assinatura
from rsa_oeap import cifrar_oaep, decifrar_oaep

N_BITS = 1024

"""
EXEMPLOS DE INPUTS:
Localizacao do tesouro em XY
Exemplo de mensagem secreta
Senha do cofre de fulano
13 homens e um segredo
"""

plaintext = input("Digite um texto para ser enviado ao receptor: \n")
p1 = gerarPrimo(N_BITS)
p2 = gerarPrimo(N_BITS)

chave_publica, chave_privada = chavesRSA(p1, p2)

print("\nMensagem Original: ", plaintext)

assinatura = assinar(plaintext, chave_publica)

print(f"\nAssinatura: {assinatura}")

texto_cifrado_oaep = cifrar_oaep(plaintext.encode('utf-8'), chave_publica)
print("\nMensagem Cifrada: ", texto_cifrado_oaep)

plaintext = decifrar_oaep(texto_cifrado_oaep, chave_privada)

print("\nMensagem Decifrada: ", plaintext.decode('utf-8'))

verificar_assinatura(assinatura, plaintext, chave_privada)