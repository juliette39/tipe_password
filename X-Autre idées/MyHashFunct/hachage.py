import hashlib
mot = "QWERTY"

print(hashlib.md5(mot.encode()).hexdigest())
