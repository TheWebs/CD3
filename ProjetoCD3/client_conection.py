import json
from threading import Thread, Timer

import time

from cache import Cache
from response import Response

"""
GET /path/file.html HTTP/1.1
Host: www.host1.com:80
[blank line here]
"""

"""
HTTP/1.1 200 OK
Date: Fri, 31 Dec 1999 23:59:59 GMT
Content-Type: text/plain
Content-Length: 42
"""


class ClientConnection(Thread):

    cache = Cache

    def __init__(self, client_connection):
        Thread.__init__(self)
        self.client_connection = client_connection
        self.request = ""
        self.response = ""
        self.running = True
        self.timer = ""

    def run(self):
        while self.running:
            try:
                self.start_timer()
                self.request = self.client_connection.recv(1024).decode()
                self.reset_timer()
                self.response = self.handle_request(self.request)
                try:
                    print("Response: \n" + self.response.decode())
                except UnicodeDecodeError:
                    print("Imagem devolvida")
                self.client_connection.sendall(self.response)
            except ConnectionAbortedError or ConnectionResetError:
                print("Client disconected!")
                self.reset_timer()
                self.running = False
        self.client_connection.close()

    def handle_request(self, request):
        parsed_request = {"method": "", "filename": "", "version": ""}
        response = Response()
        try:
            campos = request.split(" ")
            parsed_request["method"] = campos[0]
            parsed_request["filename"] = campos[1]
            parsed_request["version"] = campos[2]
            # print(request)
            print("Request: " + parsed_request["method"] + " " + parsed_request["filename"])
        except:
            response.set_bad_request()
            return response.to_string()
        if parsed_request["method"] not in ["GET", "HEAD", "POST"]:
            response.set_bad_request()
            return response.to_string()
        # TODO: VERIFICAR SE É UM POST
        if parsed_request["filename"] == '/':
            parsed_request["filename"] = '/index.html'
        if "private" in parsed_request["filename"].split("/"):
            response.set_forbidden()
            return response.to_string()
        try:
            file = open("htdocs" + parsed_request["filename"], "rb")
            response.body = file.read()
        except FileNotFoundError:
            response.set_not_found()
            return response.to_string()
        response.set_ok()
        if ".jpg" in parsed_request["filename"]:
            response.headers.append("Content-Type: image/jpeg")
        if ".png" in parsed_request["filename"]:
            response.headers.append("Content-Type: image/png")
        if ".html" in parsed_request["filename"]:
            response.headers.append("Content-Type: text/html")
        if parsed_request["method"] == "POST":
            data = request.split("\n")
            try:
                response.body = self.handle_post_data(data[len(data)-1], response.body)
            except IndexError:
                response.set_bad_request()
                return response.to_string()
        response.headers.append("Content-Length: " + str(len(response.body)))
        if parsed_request["method"] == "HEAD":
            response.body = b''
        if parsed_request["filename"] not in Cache.get_top_two():
            time.sleep(1/10)
            print("[" + parsed_request["filename"] + "] Ficheiro nao esta em cache")
            # print(Cache.cache) # LIGAR ESTA LINHA E LINHA ABAIXO PARA FAZER DEBUG NA CACHE
        # print(Cache.get_top_two())
        Cache.add_to_count(parsed_request["filename"])
        return response.to_string()

    def start_timer(self):
        self.timer = Timer(10, self.end_connection)
        self.timer.start()

    def reset_timer(self):
        self.timer.cancel()

    def end_connection(self):
        self.client_connection.close()

    def handle_post_data(self, data, current_body):
        temporary_dict = {}
        pares = data.split("&")
        for par in pares:
            print(par)
            dados = par.split("=")
            temporary_dict[dados[0]] = dados[1]
        return b''.join([current_body, json.dumps(temporary_dict).encode()])
