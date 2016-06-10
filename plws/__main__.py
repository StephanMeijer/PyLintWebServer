import time
import json

from http.server import HTTPServer
from urllib.parse import parse_qs
from cgi import parse_header, parse_multipart

from github_webhook_server import GithubWebHookServer

config = json.load(open('config.json'))

hostName = config['hostName']
hostPort = config['hostPort']

server = HTTPServer((hostName, hostPort), GithubWebHookServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
