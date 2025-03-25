import hashlib

def calculate_sha256_hash(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))  # Chuyển đổi dữ liệu thành bytes
    return sha256_hash.hexdigest()  # Trả về biểu diễn hex của chuỗi hash

data_to_hash = input("Nhập chuỗi cần băm SHA-256: ")
hash_value = calculate_sha256_hash(data_to_hash)
print(f"Chuỗi '{data_to_hash}' có mã băm SHA-256: {hash_value}")
