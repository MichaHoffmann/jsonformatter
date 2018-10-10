from unittest import TestCase
from parameterized import parameterized

from lib.visitors.PathVisitor import PathVisitor
from lib.visitors.PrettyVisitor import PrettyVisitor
from lib.JSONTree import JSONTree


class TestPathVisitor(TestCase):

    @parameterized.expand([
        ['a.b', ["a", "b"]],
        ['a.b.c', ["a", "b", "c"]],
        ['a.x["b.c"].d', ["a", "x", "b.c", "d"]],
        ['a["b.c[d]"].e', ["a", "b.c[d]", "e"]],
        ['a["b"]["c"]', ["a", "b", "c"]]
    ])
    def test_parse_path(self, path, res):
        self.assertListEqual(PathVisitor.parse_path(path), res)

    @parameterized.expand([
        ['foo.0', '{"foo":["bar","baz"]}', '"bar"'],
        ['foo.1', '{"foo":["bar","baz"]}', '"baz"'],
        ['foo', '{"foo":["bar","baz"]}', '["bar","baz"]']
    ])
    def test_path_visitor(self, path, json, expect):
        tree = JSONTree.from_string(json)
        res = tree.accept(PathVisitor(path)).accept(PrettyVisitor(True, False))
        self.assertEqual(res, expect)
