import random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class DiffieHellmanParty:
    q = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371
    alpha = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5
    iv = b'\x00'*16 #TODO: should be random
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.shared_secret = None
        self.aes_key = None
    def gen_keys(self):
        self.private_key = random.randint(0, self.q)
        self.public_key = pow(self.alpha, self.private_key, self.q)
    def compute_shared_secret(self, other_public_key):
       self.shared_secret = pow(other_public_key, self.private_key, self.q)
    def get_aes_key(self):
       #convert secret to bytes for hashing. +7 so we round up, // 8 converts bits to bytes, 'big' for
       #big endian byte order
       s_bytes = self.shared_secret.to_bytes((self.shared_secret.bit_length() + 7) // 8, 'big')
       #hash
       sha = SHA256.new(data=s_bytes)
       sha_hash = sha.digest()
       self.aes_key = sha_hash[:16]
    def encrypt(self, plaintext, iv):
       cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
       padded_msg = pad(plaintext.encode('utf-8'), AES.block_size)
       ciphertext = cipher.encrypt(padded_msg)
       return ciphertext
    def decrypt(self, ciphertext, iv):
       cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
       padded_msg = cipher.decrypt(ciphertext)
       plaintext = unpad(padded_msg, AES.block_size).decode('utf-8')
       return plaintext
