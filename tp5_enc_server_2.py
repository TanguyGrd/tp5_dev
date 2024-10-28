import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()
client, client_addr = sock.accept()

def binToSigns(signsInt):
    result = ""
    valueSign = signsInt & 0b1
    if valueSign == 0b0:
        result = "-"
    signsInt = signsInt >> 1
    if signsInt == 0b01:
        result = "-" + result
    elif signsInt == 0b10:
        result = "*" + result
    else:
        result = "+" + result
    return result

def dataToCalcul(data):
    value1 = data >> 24
    value2 = 0xFFFFFF & data
    value1_signs_bin = value1 >> 20
    value1 = str(0xFFFFF & value1)
    value1_signs = binToSigns(value1_signs_bin)
    value2_signs_bin = value2 >> 20
    value2 = str(0xFFFFF & value2)
    value2_signs = binToSigns(value2_signs_bin)
    return value1_signs + value1 + value2_signs + value2

while True:
    header = client.recv(1)
    if not header:
        break

    msg_len = int.from_bytes(header, byteorder='big')
    chunks = []
    bytes_received = 0
    while bytes_received < msg_len:
        chunk = client.recv(min(msg_len - bytes_received, 1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received')

        chunks.append(chunk)
        bytes_received += len(chunk)

    value_data = int.from_bytes(chunks[0], byteorder='big')
    calcul = dataToCalcul(value_data)
    client.send((f"Le résultat est {eval(calcul)}").encode())

client.close()
sock.close()
