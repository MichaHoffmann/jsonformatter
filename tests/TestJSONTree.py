import unittest
from xml.etree import ElementTree

from lib.JSONTree import JSONTree, JSONDictNode, JSONListNode


class TestJSONTreeFromString(unittest.TestCase):
    def test_from_string_1(self):
        json_tree = JSONTree.from_string('{"a": "b"}')
        self.assertTrue(isinstance(json_tree, JSONDictNode))

    def test_from_string_1_number_of_children(self):
        json_tree = JSONTree.from_string('{"a": "b"}')
        self.assertEqual(len(json_tree.children), 1)

    def test_from_string_with_list_child_1(self):
        json_tree = JSONTree.from_string('{"a": ["b", "c"]}')
        self.assertEqual(len(json_tree.children), 1)

    def test_from_string_with_list_child_correct_type(self):
        json_tree = JSONTree.from_string('{"a": ["b", "c"]}')
        self.assertTrue(isinstance(json_tree.children["a"], JSONListNode))

    def test_from_string_with_list_child_number_items(self):
        json_tree = JSONTree.from_string('{"a": ["b", "c"]}')
        self.assertEqual(len(json_tree.children["a"].children), 2)


class TestJSONTreeFormattingSimpleDict(unittest.TestCase):
    def setUp(self):
        self.json_tree = JSONTree.from_string('{"a": "b"}')

    def test_flatten(self):
        expected_flattened_tree = 'data.a = "b"\n'
        self.assertEqual(expected_flattened_tree, self.json_tree.flatten())

    def test_html(self):
        expected_htmlized_tree = \
            '<table border="1"><caption>Object</caption><tbody>\n' \
            '    <tr><th>Name</th><th>Value</th></tr>\n' \
            '    <tr>\n' \
            '        <td align="center">\n' \
            '            a\n' \
            '        </td>\n' \
            '        <td align="center">\n' \
            '            b\n' \
            '        </td>\n' \
            '    </tr>\n' \
            '</tbody></table>\n'
        self.assertEqual(expected_htmlized_tree, self.json_tree.htmlize())


class TestJSONTreeFormattingNestedDict(unittest.TestCase):
    def setUp(self):
        self.json_tree = JSONTree.from_string('{"a": ["b", {"c": "d"}]}')

    def test_flatten(self):
        expected_flattened_tree = 'data.a[0] = "b"\ndata.a[1].c = "d"\n'
        self.assertEqual(expected_flattened_tree, self.json_tree.flatten())

    def test_htmlize_root_is_table(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual(htmlroot.tag, 'table')

    def test_htmlize_table_has_caption_and_body(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual(list(map(lambda e: e.tag, list(htmlroot))), [
                         'caption', 'tbody'])

    def test_htmlize_tablebody_has_table_from_list(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual('List', htmlroot.findall(
            './tbody/tr/td/table/caption')[0].text)

    def test_htmlize_outermost_table_key(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual('a', htmlroot.findall(
            './tbody/tr/td')[0].text.strip())

    def test_htmlize_outermost_table_val(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual('table', htmlroot.findall(
            './tbody/tr/td/table')[0].tag)

    def test_htmlize_innermost_table_exists(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual('table', htmlroot.findall(
            './tbody/tr/td/table/tbody/tr/td/table')[0].tag)

    def test_htmlize_innermost_table_key(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual('c', htmlroot.findall(
            './tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td')[0].text.strip())

    def test_htmlize_innermost_table_value(self):
        htmlroot = ElementTree.fromstring(self.json_tree.htmlize())
        self.assertEqual('d', htmlroot.findall(
            './tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td')[1].text.strip())
