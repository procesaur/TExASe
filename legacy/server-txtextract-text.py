from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from subprocess import Popen, DEVNULL, STDOUT
from redis import Redis
from rq import Queue
from long_run4 import rq_handler

q = Queue(connection=Redis())


class MyServer(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        self.send_response(200)
        self.wfile.write(
            bytes("Python server running...\n\nAll your base are belong to us.\nFeed your strings here.", "utf-8"))

    # POST
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode("utf-8")
        print('Received: ' + data + '\nText extraction started...')
        # Popen(['python3', 'long_run.py', data], stdout=DEVNULL, stderr=STDOUT)
        # Popen(['python3', '/usr/legacy/long_run2.py', data])
        result = q.enqueue(rq_handler, data)
        print(time.asctime(), "Server Listening @ %s:%s" % (hostName, hostPort))


if __name__ == '__main__':
    hostName = "localhost"
    hostPort = 12346

    myServer = HTTPServer((hostName, hostPort), MyServer)
    print(time.asctime(), "Server Started @ %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stopped @ %s:%s" % (hostName, hostPort))
