"""
Entry point for command line execution mode.
"""

import shellish
import yaml
from . import commands
from shellish.command import contrib


class Root(shellish.Command):
    """ Flota (spanish for fleet) - A Docker CLI """

    name = 'flota'

    def setup_args(self, parser):
        self.add_subcommand(commands.ps.Entry)
        self.add_subcommand(commands.misc.Debug)
        self.add_subcommand(contrib.Exit)
        self.add_subcommand(contrib.Help)

    def run(self, args):
        self.session.run_loop()

    def get_credentials(self, args):
        """ Triage credential fetch; Command line arg, INI, or prompt. """
        domain, key, sched = args.pd_domain, args.pd_apikey, args.pd_schedule
        if domain and key and sched:
            return domain, key, sched
        pd_config = self.get_config('pd')
        if not domain:
            domain = pd_config.get('domain') or input('PagerDuty Domain: ')
        if not key:
            key = pd_config.get('apikey') or \
                  getpass.getpass('PagerDuty API Key: ')
        if not sched:
            sched = pd_config.get('schedule') or \
                    input('PagerDuty Schedule ID: ')
        if not (domain and key and sched):
            raise TypeError('PagerDuty Domain, API Key and Schedule are '
                            'required')
        return domain, key, sched


def main():
    root = Root()
    args = root.parse_args()
    host = os.getenv('DOCKER_HOST')
    tlsopts = {}
    if not host:
        url = 'unix+http://var/run/docker.sock'
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
    print('url', url, tlsopts)
    root.inject_context({
        "url": url,
        "tlsopts": tlsopts
    })
    root(args)
