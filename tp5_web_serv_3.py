import socket
import re
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()

HTML_MODELS = "./htdocs/"

print("Serveur lancé")

def read_html(filename) -> str:
    file_content = ""
    with open(f'{HTML_MODELS}/{filename}', encoding="UTF-8") as file:
        file_content = file.read()
    return file_content

while True:
    client, client_addr = sock.accept()
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

            if ".html" not in REQUEST:
                REQUEST += ".html"

            REQUEST = REQUEST[1:]
            if os.path.isfile(f'{HTML_MODELS}/{REQUEST}'):
                html_content = read_html(REQUEST)
                RESPONSE = "HTTP/1.0 200 OK\n\n" + html_content
            else:
                html_content = read_html("404.html")
                RESPONSE = "HTTP/1.0 404 Not Found\n\n" + html_content
        else:
            html_content = read_html("400.html")
            RESPONSE = "HTTP/1.0 400 Bad Request\n\n" + html_content

        client.send(RESPONSE.encode("UTF-8"))
        break
    client.close()

sock.close()
