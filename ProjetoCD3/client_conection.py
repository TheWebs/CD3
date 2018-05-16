from threading import Thread

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

    def __init__(self, client_connection):
        self.client_connection = client_connection
        self.request = ""
        self.response = ""
        self.running = True

    def run(self):
        while self.running:
            self.request = self.client_connection.recv(1024).decode()
            self.response = self.handle_request(self.request)
            print(self.response.decode())
            self.client_connection.sendall(self.response)
        self.client_connection.close()

    def handle_request(self, request):
        parsed_request = {"method": "", "filename": "", "version": ""}
        response = Response()
        try:
            campos = request.split(" ")
            parsed_request["method"] = campos[0]
            parsed_request["filename"] = campos[1]
            parsed_request["version"] = campos[2]
        except:
            response.set_bad_request()
            return response.to_string()
        if parsed_request["method"] not in ["GET", "POST"]:
            response.set_bad_request()
            return response.to_string()
        if parsed_request["filename"] == '/':
            parsed_request["filename"] = '/index.html'
        try:
                file = open("htdocs" + parsed_request["filename"], "rb")
                response.body = file.read()
        except FileNotFoundError:
                response.set_not_found()
                return response.to_string()
        response.status = "200 Ok"
        if ".jpg" in parsed_request["filename"]:
            response.headers.append("Content-Type: image/jpeg")
        if ".png" in parsed_request["filename"]:
            response.headers.append("Content-Type: image/png")
        if ".html" in parsed_request["filename"]:
            response.headers.append("Content-Type: text/html")
        response.headers.append("Content-Length: " + str(len(str(response.body))))
        return response.to_string()

"""!!!TODO: SE TEXTO LER EM MODO NAO BYTES!!!"""