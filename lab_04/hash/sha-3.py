from Crypto.Hash import SHA3_256

def sha3(message):
    sha3_hash = SHA3_256.new()
    sha3_hash.update(message.encode('utf-8'))
    return sha3_hash.hexdigest()

def main():
    text = input("Nhập chuỗi văn bản: ")
    hashed_text = sha3(text)
    print("Chuỗi văn bản đã nhập:", text)
    print("SHA-3 Hash:", hashed_text)

if __name__ == "__main__":
    main()
