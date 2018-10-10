import argparse
import sys

from lib.JSONTree import JSONTree
from lib.visitors.PrettyVisitor import PrettyVisitor
from lib.visitors.PathVisitor import PathVisitor

parser = argparse.ArgumentParser(description='Sample JSON Formatter')

parser.add_argument('-path', help='Json Path', action='store', dest='path')
parser.add_argument('-color', action='store_true', dest='color', default=False)
parser.add_argument('-compact', action='store_true',
                    dest='compact', default=False)


arguments = parser.parse_args()

try:
    tree = JSONTree.from_string(sys.stdin.read())
    if arguments.path:
        tree = tree.accept(PathVisitor(arguments.path))

    print(tree.accept(PrettyVisitor(arguments.compact, arguments.color)))
except IOError as e:
    print('An Error occured: {}'.format(e.strerror))
