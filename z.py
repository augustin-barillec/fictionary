import hashlib

x = hashlib.md5('a'.encode()).hexdigest()


print(type(x))
print(x)
