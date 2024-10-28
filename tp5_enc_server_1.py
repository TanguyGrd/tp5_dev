import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()

FOOTER = 0

client, client_addr = sock.accept()
print(f"Connection from {client_addr} established.")

try:
    while True:
        header = client.recv(4)
        if not header:
            print("Client disconnected.")
            break

        msg_len = int.from_bytes(header, byteorder='big')
        print(f"Receiving the next {msg_len} bytes")

        chunks = []
        bytes_received = 0
        while bytes_received < msg_len:
            chunk = client.recv(min(msg_len - bytes_received, 1024))
            if not chunk:
                raise RuntimeError("Connection lost while receiving data")

            chunks.append(chunk)
            bytes_received += len(chunk)

        message_received = b"".join(chunks).decode('utf-8')
        footer_msg = client.recv(1)
        footer_data = int.from_bytes(footer_msg, byteorder='big')

        if FOOTER == footer_data:
            print(f"Received from client: {message_received}")
        else:
            print("No end sequence found")

finally:
    client.close()
    sock.close()
