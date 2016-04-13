"""
Commands related to on-call people.
"""

import collections
import datetime
import functools
import humanize
import operator
import shellish


class PS(shellish.Command):
    """ Process List. """

    name = 'ps'

    def setup_args(self, parser):
        self.add_argument('-a', '--all', action='store_true', help='Show all '
                          'containers (default shows just running)')

    def created_getter(self, container):
        now = datetime.datetime.utcnow()
        ts = datetime.datetime.utcfromtimestamp(container['Created'])
        return humanize.naturaldelta(now - ts)

    def run(self, args):
        params = {}
        if args.all:
            params['all'] = 1
        print(self, args)
        containers = self.api.get('/containers/json', params=params).json()
        fields = collections.OrderedDict((
            ('CONTAINER ID', lambda x: x['Id'][:12]),
            ('IMAGE', 'Image'),
            ('COMMAND', 'Command'),
            ('CREATED', self.created_getter),
            ('STATUS', 'Status'),
            ('PORTS', lambda x: ', '.join(x['Ports'])),
            ('NAMES', lambda x: ', '.join(x['Names'])),
        ))
        t = shellish.Table(headers=fields.keys(), accessors=fields.values())
        t.print(containers)
