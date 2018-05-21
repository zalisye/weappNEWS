
import hashlib

def main():
    data = '你好'
    m = hashlib.md5()
    m.update(data.encode())
    print(m.hexdigest())

main()
