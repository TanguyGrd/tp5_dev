import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

s.send("GET /".encode())

s_data = s.recv(1024)
print(s_data.decode())
s.close()
