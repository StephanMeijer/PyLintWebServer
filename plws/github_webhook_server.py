""" Github webhook server

@author: Stephan Meijer & Gijsbert ter Horst
"""

import json
from http.server import BaseHTTPRequestHandler
from git_handler import GitHandler


class GithubWebHookServer(BaseHTTPRequestHandler):
    """ Handles a request that passes a pull request.
    Clones the commit of the pull request.
    Runs the code through pylint
    Comments on the pull-request with the results."""

    def __init__(self, *args, **kwargs):
        with open('config.json') as configfile:
            self.config = json.load(configfile)
        super(GithubWebHookServer, self).__init__(*args, **kwargs)

    def do_POST(self):
        """ Reply to an HTTP POST """
        if not self.__authenticate():
            self.send_response(403)
            self.end_headers()
            return
        # Send response 202 Accepted
        # We've accepted the request and are processing it.
        self.send_response(202)
        try:
            post_data = json.loads(
                self.rfile.read(
                    int(self.headers['Content-Length'])).decode('utf-8'))
            if post_data['action'] not in ('opened', 'synchronize'):
                # Pull Request is no longer open.
                # Reply with HTTP 409 Conflict
                self.send_response(409)
                self.end_headers()
                return
            handler = GitHandler(post_data, self.config['module'])
            handler.clone()
            handler.pylint_and_comment(self.config)
            # Reply 201 Created, we're not using 200 OK
            # because in that case we would have to send the result of
            # processing as a reply.
            # Instead we've created a comment on Github.
            self.send_response(201)
            self.end_headers()
        except Exception as error:
            print('Something gone wrong:\n{}'.format(str(error)))
            self.send_response(500)
            self.end_headers()

    def __authenticate(self):
        #TODO: Implement
        return True
