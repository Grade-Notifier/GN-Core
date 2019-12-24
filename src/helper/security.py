from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

KEY_SIZE = 2048

def gen_keys():
    key = RSA.generate(KEY_SIZE)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)

    public_key = key.publickey().export_key()
    file_out = open("public.pem", "wb")
    file_out.write(public_key)

def encrypt(message):
    key = RSA.importKey(open('public.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message)
    return ciphertext

def decrypt(message):
    key = RSA.importKey(open('private.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.decrypt(message)
    return ciphertext

gen_keys()
cipher = encrypt(b'password')
decrypted = decrypt(cipher)
print(decrypted)

