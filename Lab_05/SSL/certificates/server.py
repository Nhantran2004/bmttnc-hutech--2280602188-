import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

# Danh sách các client đã kết nối
clients = []

def handle_client(client_socket):
    # Thêm client vào danh sách
    clients.append(client_socket)
    print("Đã kết nối với:", client_socket.getpeername())

    try:
        # Nhận và gửi dữ liệu
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))

            # Gửi dữ liệu đến tất cả các client khác
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except Exception as e:
                        print(f"Lỗi khi gửi dữ liệu đến client: {e}")
                        clients.remove(client)
    except Exception as e:
        print(f"Lỗi khi xử lý client: {e}")
    finally:
        print("Đã ngắt kết nối:", client_socket.getpeername())
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server đang chờ kết nối...")

# Lắng nghe các kết nối
while True:
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Kết nối mới từ: {client_address}")

        # Tạo SSL context
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile="./certificates/server-cert.crt",
                                    keyfile="./certificates/server-key.key")
        except Exception as e:
            print(f"Lỗi khi tải chứng chỉ SSL: {e}")
            client_socket.close()
            continue

        # Thiết lập kết nối SSL
        try:
            ssl_socket = context.wrap_socket(client_socket, server_side=True)
        except Exception as e:
            print(f"Lỗi khi thiết lập kết nối SSL: {e}")
            client_socket.close()
            continue

        # Bắt đầu một luồng xử lý cho mỗi client
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
        client_thread.start()
    except KeyboardInterrupt:
        print("Server đang tắt...")
        break
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")

# Đóng server socket
server_socket.close()