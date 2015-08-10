try:
    from Crypto.Cipher import AES
except:
    import crypto
    import sys
    sys.modules['Crypto'] = crypto
    from Crypto.Cipher import AES

import base64
import os

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# the character used for padding, the value must be a multiple of BLOCK_SIZE in length.
PADDING = '{'


class AESEncryptor:

    def encrypt_secret(self, secret):
        key = self.__gen_key()
        cipher = AES.new(key)
        garble = base64.b64encode(cipher.encrypt(self.__pad(secret)))
        return (garble, key)

    def decrypt_secret(self, garble, key):
        cipher = AES.new(key)
        secret = cipher.decrypt(base64.b64decode(garble)).rstrip(PADDING)
        return secret

    def __pad(self, thingy):
        return thingy + (BLOCK_SIZE - len(thingy) % BLOCK_SIZE) * PADDING

    def __gen_key(self):
        return os.urandom(BLOCK_SIZE)
