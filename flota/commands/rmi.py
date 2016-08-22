"""
(Really) remove images.
"""

import shellish


class RMI(shellish.Command):
    """ Remove image(s). """

    name = 'rmi'
    use_pager = False

    def setup_args(self, parser):
        self.add_argument('-a', '--all', action='store_true', help='Delete '
                          'all images (included descendants)')
        self.add_argument('-v', '--verbose', action='store_true')
        self.add_argument('-f', '--force', action='store_true')
        self.add_argument('names', nargs='+', metavar='IMAGE|NAME|DIGEST')

    def run(self, args):
        images = self.api.get('/images/json?all=1').json()
        heads = []
        for name in args.names:
            for x in images:
                if x['RepoTags'] and \
                   (name in x['RepoTags'] or
                    x['Id'].split(':', 1)[-1].startswith(name)):
                    heads.append(x)
        if not heads:
            raise SystemExit("Image(s) not found")
        by_ids = dict((x['Id'], x) for x in images)
        params = {}
        if args.force:
            params['force'] = 1
        for head in heads:
            tail = head
            descendants = [head]
            while tail['ParentId']:
                tail = by_ids[tail['ParentId']]
                descendants.append(tail)
            for x in descendants:
                if args.verbose:
                    print('Removing: %s' % (x['Id']))
                resp = self.api.delete('/images/%s' % x['Id'], params=params)
                if resp.status_code == 409:
                    print('Skipped used image: %s' % x['Id'])
                elif resp.status_code == 404:
                    print('Missing image: %s' % x['Id'])
                elif resp.status_code != 200:
                    raise SystemExit(resp.json())
