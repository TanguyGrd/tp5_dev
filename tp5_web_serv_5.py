import socket
import re
import os
import logging

HOST = '127.0.0.1'
PORT = 9999
LOG_DIR = "C:/user/T/tp5_DEV"
LOG_FILE = "tp5_web_serv.log"
HTML_MODELS = "./htdocs/"

# ===== LOGGER =====
class CustomFormatter(logging.Formatter):
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_format = "%(asctime)s %(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: log_format,
        logging.INFO: log_format,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M")
        return formatter.format(record)

file_handler = logging.FileHandler(f"{LOG_DIR}/{LOG_FILE}", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M"
)
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ===== FUNCTIONS =====
def read_html(filename: str, ip: str) -> str:
    with open(f'{HTML_MODELS}/{filename}', encoding="UTF-8") as file:
        file_content = file.read()
    logging.info("Fichier %s envoyé au client %s", filename, ip)
    return file_content

def get_file_bytes(filename: str, ip: str) -> bytes:
    with open(f'{HTML_MODELS}/{filename}', 'rb') as file:
        file_content = file.read()
    logging.info("Fichier %s envoyé au client %s", filename, ip)
    return file_content

# ===== SOCKET SETUP =====
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen()
logging.info("Le serveur tourne sur %s:%d", HOST, PORT)

while True:
    client, (client_ip, client_port) = sock.accept()
    while True:
        data = client.recv(1024).decode("utf-8")
        if not data:
            break

        RESPONSE = ""
        extractGet = re.search(r"(?<=GET\s)\/?\S+", data)
        if extractGet:
            REQUEST = extractGet.group(0)

            
            if REQUEST == "/":
                REQUEST = "/index"

            if "." not in REQUEST:
                REQUEST += ".html"

            REQUEST = REQUEST[1:]
            if os.path.isfile(f'{HTML_MODELS}/{REQUEST}'):
                # === Fichiers PNG ===
                if REQUEST.endswith(".png"):
                    RESPONSE = "HTTP/1.0 200 OK\r\nContent-Type: image/png\r\n\r\n"
                    response_file = get_file_bytes(REQUEST, client_ip)
                    client.send(RESPONSE.encode("UTF-8"))
                    client.send(response_file)
                    break

                # === Fichiers HTML ===
                html_content = read_html(REQUEST, client_ip)
                RESPONSE = "HTTP/1.0 200 OK\r\n\r\n" + html_content
            else:
                html_content = read_html("404.html", client_ip)
                RESPONSE = "HTTP/1.0 404 Not Found\r\n\r\n" + html_content
        else:
            html_content = read_html("400.html", client_ip)
            RESPONSE = "HTTP/1.0 400 Bad Request\r\n\r\n" + html_content

        client.send(RESPONSE.encode("UTF-8"))
        break
    
