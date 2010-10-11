import optparse
import os
import sys

from snake.tasks import env


def load_snakefile():
    cwd = os.getcwd()
    sys.path.insert(0, cwd)
    try:
        imported = __import__('snakefile')
    except ImportError:
        print >> sys.stderr, "Error: couldn't find any snakefiles."
        exit(1)
    del sys.path[0]


def print_task_list(option, opt_str, value, parser):
    print("Task list:")
    for name in sorted(env["tasks"]):
        print " - %s" % name
    exit()


def main():
    load_snakefile()
    usage = "%prog [options] [task] ..."
    parser = optparse.OptionParser(usage="%prog [options] [task] ...")
    parser.add_option(
        "-l", "--list", action="callback", callback=print_task_list,
        help="print list of available tasks and exit")
    parser.disable_interspersed_args()
    options, args = parser.parse_args()
    if not args:
        args = ['default']
    for name in args:
        task = env["tasks"].get(name)
        if not task:
            print >> sys.stderr, "Error: task %r was not found." % name
            exit(1)
        task()