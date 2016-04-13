"""
Commands related to on-call people.
"""

import collections
import datetime
import humanize
import shellish


class PS(shellish.Command):
    """ Process List. """

    name = 'ps'
    use_pager = True

    def setup_args(self, parser):
        self.add_argument('-a', '--all', action='store_true', help='Show all '
                          'containers (default shows just running)')
        self.table_options = self.add_table_arguments()

    def created_getter(self, container):
        now = datetime.datetime.utcnow()
        ts = datetime.datetime.utcfromtimestamp(container['Created'])
        return humanize.naturaldelta(now - ts)

    def port_render(self, desc):
        container = '%s/%s' % (desc['PrivatePort'], desc['Type'])
        if 'IP' in desc:
            return '%s:%s=>%s' % (desc['IP'], desc['PublicPort'], container)
        else:
            return container

    def names_getter(self, container):
        return ', '.join(map(lambda x: x.lstrip('/'), container['Names']))

    def image_getter(self, container):
        image = container['Image']
        return image[7:19] if image.startswith('sha256:') else image

    def run(self, args):
        params = {}
        if args.all:
            params['all'] = 1
        containers = self.api.get('/containers/json', params=params).json()
        fields = collections.OrderedDict((
            ('CONTAINER ID', lambda x: x['Id'][:12]),
            ('IMAGE', self.image_getter),
            ('COMMAND', 'Command'),
            ('CREATED', self.created_getter),
            ('STATUS', 'Status'),
            ('PORTS', lambda x: ', '.join(map(self.port_render, x['Ports']))),
            ('NAMES', self.names_getter)
        ))
        colspec = (12, ) + (None,) * 6
        t = shellish.Table(headers=fields.keys(), accessors=fields.values(),
                           columns=colspec, **self.table_options(args))
        t.print(containers)
