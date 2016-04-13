"""
Commands related to on-call people.
"""

import collections
import functools
import operator
import shellish
import pygerduty
from .. import rotation


class PS(shellish.Command):
    """ Process List. """

    name = 'ps'

    def run(self, args):
        print (self, args)
        if self.rotation is None:
            raise SystemExit('No people specification to show')
        days_as_text = lambda x: ','.join((rotation.Person.days[i] for i in x))
        fields = collections.OrderedDict((
            ('PD User ID', operator.attrgetter('pd_user_id')),
            ('Name', self.fetch_from_user('name')),
            ('Email', self.fetch_from_user('email')),
            ('Req SR', operator.attrgetter('service_ratio')),
            ('Rel SR',
             lambda x: '%.0f%%' % (self.rotation.rel_service_ratio(x) * 100)),
            ('ON Prefs', lambda x: days_as_text(x.on_prefs)),
            ('OFF Prefs', lambda x: days_as_text(x.off_prefs)),
        ))
        t = shellish.Table(headers=fields.keys(), accessors=fields.values())
        t.print(self.rotation.people)

    @functools.lru_cache()
    def get_user(self, user_id):
        try:
            return self.pd.users.show(user_id)
        except pygerduty.BadRequest:
            return

    def fetch_from_user(self, field):
        """ Return an accessor function that gets data from the pagerduty
        users api. """

        def getter(x):
            user = self.get_user(x.pd_user_id)
            return getattr(user, field) if user else '<red>invalid user_id</red>'
        return getter
