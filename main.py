import argparse
import os
import sys

from lib.JSONTree import JSONTree

parser = argparse.ArgumentParser(description='Sample JSON Formatter')

parser.add_argument('-htmlize', help='Convert JSON at path into a nested HTML Table',
                    action='store_true', dest='htmlize', default=False)
parser.add_argument('-flatten', help='Convert JSON at path into a flattened Key Value List',
                    action='store_true', dest='flatten', default=False)

parser.add_argument('-pretty', help='Pretty Print the input json',
                    action='store_true', dest='pretty', default=False)

parser.add_argument('-path', help='Specify the path to the JSON File',
                    action='store', dest='path', required=True)

arguments = parser.parse_args()
filepath = os.path.normpath(arguments.path)

try:
    with open(filepath, 'r') as f:
        json_tree = JSONTree.from_string(f.read())
        if arguments.htmlize:
            print(json_tree.htmlize())
        if arguments.flatten:
            print(json_tree.flatten())
        if arguments.pretty:
            print(json_tree.pretty())
except IOError as e:
    print('An Error occured: {}'.format(e.strerror))
