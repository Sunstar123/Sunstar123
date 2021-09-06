# import cryptography
from cryptography.fernet import Fernet


# help(cryptography)
key = Fernet.generate_key()
k = Fernet(key)
print(len(key), "next:", k)
num = 100 ** 40
num2 = 10 ** 15
print(num/num2)
plain = b"bajh"
# print(plain)
unusable = k.encrypt(plain)
# print(len(unusable))
usable = k.decrypt(unusable)
# print(usable)
if plain == usable:
    print("success")
else:
    print("failure")
