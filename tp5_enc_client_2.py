import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

def is_calcul(value: str):
    return re.search(r'^([\-+]?\d+)\s*[\+\-\*]\s*([\-+]?\d+)$', value)

def parse_numbers(msg):
    return re.findall(r'([+-]?\d+)', msg)

def check_byte_limit(msg):
    numbers = parse_numbers(msg)
    return 0 == len([int(x) for x in numbers if abs(int(x)) > 1048575])

def parse_expression(msg):
    return re.findall(r'([+\-]?\d+|[+\-\*\/]{1,2}\d+)', msg)

def extract_signs(val):
    return re.findall(r'([+\-*]+)?(\d+)', val)[0]

def signs_to_bin(signs):
    result = 0
    if len(signs) >= 1:
        if signs[0] == '-':
            result += 0b01
        elif signs[0] == '*':
            result += 0b10
        result = result << 1
    result += 0b1
    if len(signs) > 1 and signs[1] == '-':
        result -= 0b1
    return result

def calcul_to_byte(msg):
    values = parse_expression(msg)
    values_unsigned = [extract_signs(v) for v in values]
    result = bytes()
    final_length = 0
    for signs, val in values_unsigned:
        val = int(val)
        signs_int = signs_to_bin(signs)
        signs_int = signs_int << 20
        final_int = signs_int | val
        final_bytes = final_int.to_bytes(3, 'big')
        result += final_bytes
        final_length += len(final_bytes)
    return result, final_length

msg = input("Calcul à envoyer: ")

if not is_calcul(msg):
    raise ValueError("Mauvais calcul")

if not check_byte_limit(msg):
    raise ValueError("Valeur trop grande")

encoded_msg, encoded_msg_length = calcul_to_byte(msg)
header = encoded_msg_length.to_bytes(1, byteorder='big')
payload = header + encoded_msg

s.send(payload)

s_data = s.recv(1024)
print(s_data.decode())
s.close()
