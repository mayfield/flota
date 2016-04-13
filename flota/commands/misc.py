"""
Misc commands.
"""

import code
import shellish


class Debug(shellish.Command):
    """ Run an interactive python interpretor. """

    name = 'debug'
    use_pager = False

    def run(self, args):
        env = self.__dict__.copy()
        env['args'] = args
        code.interact(None, None, env)
