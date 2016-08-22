"""
List images
"""

import collections
import datetime
import humanize
import shellish


class Images(shellish.Command):
    """ List images. """

    name = 'images'
    use_pager = True

    def setup_args(self, parser):
        self.add_argument('-a', '--all', action='store_true', help='Show all '
                          'images (default shows just tagged)')
        self.add_argument('-q', '--quiet', action='store_true', help='Only '
                          'the image ID')
        self.add_argument('names', nargs='*', metavar='IMAGE|NAME')
        self.table_options = self.add_table_arguments()

    def created_getter(self, image):
        now = datetime.datetime.utcnow()
        ts = datetime.datetime.utcfromtimestamp(image['Created'])
        return '%s ago' % humanize.naturaldelta(now - ts)

    def name_getter(self, image, fallback='<none>'):
        if not image['RepoTags']:
            return fallback
        tags = [x if x!= '<none>:<none>' else fallback
                for x in image['RepoTags']]
        return ','.join(tags)

    def size_getter(self, image):
        return humanize.naturalsize(image['Size'], format='%.0f')

    def label_getter(self, image):
        if image['Labels']:
            return ','.join('%s=%s' for x in image['Labels'])
        else:
            return ''

    def parent_getter(self, image):
        fallback = image['ParentId'].split(':', 1)[-1][:12]
        if image['ParentId'] in self.by_id:
            parent = self.by_id[image['ParentId']]
            return self.name_getter(parent, fallback=fallback)
        else:
            return fallback

    def run(self, args):
        params = {}
        if args.all:
            params['all'] = 1
        images = self.api.get('/images/json', params=params).json()
        self.by_id = dict((x['Id'], x) for x in images)
        fields = collections.OrderedDict((
            ('Name', self.name_getter),
            ('ID', lambda x: x['Id'].split(':', 1)[-1][:12]),
            ('Parent', self.parent_getter),
            ('Created', self.created_getter),
            ('Labels', self.label_getter),
            ('Size', self.size_getter),
        ))
        colspec = (
            None,
            12,
            None,
            None,
            None,
            None,
        )
        t = shellish.Table(headers=fields.keys(), accessors=fields.values(),
                           columns=colspec, **self.table_options(args))
        t.print(images)
