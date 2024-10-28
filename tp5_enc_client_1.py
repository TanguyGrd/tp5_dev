import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

def is_calcul(value: str):
    return re.search(r'^(-?\d+)\s*[\+\-\*]\s*(-?\d+)$', value)

def check_byte_limit(l: list):
    return 0 == len([int(x) for x in l if abs(int(x)) >= 1048575])

msg = input("Calcul à envoyer: ")
if not is_calcul(msg):
    raise ValueError("Mauvais calcul")

values = re.split(r"\s*[\+\-\*]\s*", msg)
if not check_byte_limit(values):
    raise ValueError("Valeur trop grande")

msg_len = len(msg)
END = 0
encoded_msg = msg.encode('utf-8')

header = msg_len.to_bytes(4, byteorder='big')
footer = END.to_bytes(4, byteorder='big')
payload = header + encoded_msg + footer

s.send(payload)

s_data = s.recv(1024)
print(s_data.decode())
s.close()
