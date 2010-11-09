import inspect
import optparse
from snake.tasks.base import BaseTask


class Command(BaseTask):

    usage = '%%prog [global_options] %s [options]'

    def __init__(self, name, snake, prerequisites=None, options=None, func=None):
        super(Command, self).__init__(
            name, snake, prerequisites=prerequisites, func=func)
        self.parser = optparse.OptionParser(usage=self.usage % self.name)
        if options:
            self.takes(*options)

    def _add_options(self, options):
        for option in options:
            if isinstance(option, (list, tuple)):
                dest = option[0]
                name = '--%s' % dest.replace('_', '-')
                help = option[1]
                self.parser.add_option(name, dest=dest, help=help)
            elif isinstance(option, optparse.Option):
                self.parser.add_option(option)
            else:
                raise Exception("Uknown object type provided as option.")

    def takes(self, *options, **kwargs):
        if kwargs.get('replace', False):
            self.parser.option_list = []
        self._add_options(options)

    def __call__(self, args):
        self.call(*self.parser.parse_args(args))

    def call(self, options, args):
        if self.func:
            if len(inspect.getargspec(self.func)[0]):
                self.func(self, options, args)
            else:
                self.func()
