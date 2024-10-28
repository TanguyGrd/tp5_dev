import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()

print("Serveur lancé")

while True:
    client, client_addr = sock.accept()
    while True:
        data = client.recv(1024).decode("utf-8")
        if not data:
            break

        RESPONSE = ""
        if "GET /" in data:
            RESPONSE = "HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>"
        client.send(RESPONSE.encode())

        break

    client.close()
sock.close()
