"""
List container "processes".
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
        return '%s ago' % humanize.naturaldelta(now - ts)

    def port_render(self, desc):
        if desc['Type'] == 'tcp':
            container = str(desc['PrivatePort'])
        else:
            container = '%s/%s' % (desc['PrivatePort'], desc['Type'])
        if 'IP' in desc:
            if desc['IP'] == '0.0.0.0':
                desc['IP'] = '*'
            return '%s:%s=>%s' % (desc['IP'], desc['PublicPort'], container)
        else:
            return container

    def name_getter(self, container):
        name = ', '.join(map(lambda x: x.lstrip('/'), container['Names']))
        return name or container['Id'][:12]

    def image_getter(self, container):
        image = container['Image']
        return image[7:19] if image.startswith('sha256:') else image

    def run(self, args):
        params = {}
        if args.all:
            params['all'] = 1
        containers = self.api.get('/containers/json', params=params).json()
        fields = collections.OrderedDict((
            ('NAME', self.name_getter),
            ('IMAGE', self.image_getter),
            ('COMMAND', lambda x: x['Command'].split()[0]),
            ('CREATED', self.created_getter),
            ('STATUS', 'Status'),
            ('PORTS', lambda x: ', '.join(map(self.port_render, x['Ports']))),
        ))
        t = shellish.Table(headers=fields.keys(), accessors=fields.values(),
                           **self.table_options(args))
        t.print(containers)
