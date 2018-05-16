import time


class Response:

    def __init__(self):
        self.version = "HTTP/1.1"
        self.status = ""
        self.body = ""
        self.headers = []

    def set_bad_request(self):
        self.status = "400 Bad Request"

    def set_not_found(self):
        self.status = "404 Not Found"

    def to_string(self):
        response = self.version + " " + self.status + "\n" + time.strftime("%c") + "\nServer: Custom 1.0"
        for header in self.headers:
            response += "\n" + header
        response += "\n"
        response += str(self.body)
        response = response.encode()
        return response

"""
HTTP/1.1 200 OK
Date: Fri, 31 Dec 1999 23:59:59 GMT
Content-Type: text/plain
Content-Length: 42
"""

"""
HTTP/1.1 404 Not Found
Date: Sun, 18 Oct 2012 10:36:20 GMT
Server: Apache/2.2.14 (Win32)
Content-Length: 230
Connection: Closed
Content-Type: text/html; charset=iso-8859-1
"""