"""
Entry point for command line execution mode.
"""

import os
import requests_unixsocket as requests
import shellish
from .commands import *
from shellish.command import contrib


class Root(shellish.Command):
    """ Flota (spanish for fleet) - A Docker CLI """

    name = 'flota'

    def setup_args(self, parser):
        self.add_subcommand(images.Images)
        self.add_subcommand(ps.PS)
        self.add_subcommand(rmi.RMI)
        self.add_subcommand(misc.Debug)
        self.add_subcommand(contrib.Exit)
        self.add_subcommand(contrib.Help)

    def run(self, args):
        self.session.run_loop()


class DockerSession(requests.Session):

    def __init__(self, url, tlsopts):
        self.url = url
        self.tlsopts = tlsopts
        super().__init__()

    def request(self, method, url, *args, **kwargs):
        options = self.tlsopts.copy()
        options.update(kwargs)
        return super().request(method, self.url + url, *args, **options)


def main():
    host = os.getenv('DOCKER_HOST')
    tlsopts = {}
    if not host:
        url = 'http+unix://%2Fvar%2Frun%2Fdocker.sock'
    else:
        secure = bool(int(os.getenv('DOCKER_TLS_VERIFY', 0)))
        if secure:
            proto = 'https'
            certpath = os.getenv('DOCKER_CERT_PATH')
            tlsopts = {
                "cert": ('%s/cert.pem' % certpath, '%s/key.pem' % certpath),
                "verify": '%s/ca.pem' % certpath
            }
        else:
            proto = 'http'
        url = '%s://%s' % (proto, host.split('://', 1)[1])
    root = Root()
    root.inject_context(api=DockerSession(url, tlsopts))
    root()
