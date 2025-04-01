import sys
from PIL import Image

def encode_image(image_path, message):
    """
    Mã hóa thông điệp vào hình ảnh bằng kỹ thuật steganography.
    """
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp hình ảnh '{image_path}'.")
        return

    width, height = img.size

    # Chuyển thông điệp thành chuỗi nhị phân
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Dấu kết thúc
    data_index = 0

    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))

            for color_channel in range(3):  # Duyệt qua các kênh màu (R, G, B)
                if data_index < len(binary_message):
                    # Thay đổi bit cuối cùng của kênh màu
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1

            img.putpixel((col, row), tuple(pixel))

            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    # Lưu hình ảnh đã mã hóa
    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print("Steganography complete. Encoded image saved as", encoded_image_path)


def main():
    """
    Hàm chính để xử lý đầu vào từ dòng lệnh.
    """
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)


if __name__ == "__main__":
    main()