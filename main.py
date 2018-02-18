import sys
import os

from project.lib.JSONTree import JSONTree

filepath = os.path.normpath(sys.argv[1])

with open(filepath, 'r') as f:
    json_tree = JSONTree.from_string(f.read())
    print(json_tree.htmlize())
    print(json_tree.flatten())
