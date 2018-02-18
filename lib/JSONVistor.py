from abc import ABCMeta, abstractmethod


class JSONVisitor(object):
    __meta__ = ABCMeta

    @abstractmethod
    def visit_base(self, node):
        pass

    @abstractmethod
    def visit_list(self, node):
        pass

    @abstractmethod
    def visit_dict(self, node):
        pass


class JSONFlattenVisitor(JSONVisitor):
    def __init__(self):
        self.prefix = 'data'

    def visit_dict(self, node):
        res = ''
        tmp_prefix = self.prefix
        for key, child in node.children.items():
            self.prefix += '.{}'.format(key)
            res += child.accept(self)
            self.prefix = tmp_prefix
        return res

    def visit_list(self, node):
        res = ''
        tmp_prefix = self.prefix
        for key, child in node.children.items():
            self.prefix += '[{}]'.format(key)
            res += child.accept(self)
            self.prefix = tmp_prefix
        return res

    def visit_base(self, node):
        return '{} = "{}"\n'.format(self.prefix, node.val)


class JSONHtmlVisitor(JSONVisitor):
    def __init__(self):
        self.tabs = 0

    def visit_node(self, node, key, res):
        self.tabs += 3
        content = node.accept(self)
        self.tabs -= 3
        res += '{indent}<tr>\n' \
               '{indent}    <td align="center">\n' \
               '{indent}        {key}\n' \
               '{indent}    </td>\n' \
               '{indent}    <td align="center">\n' \
               '{content}' \
               '{indent}    </td>\n' \
               '{indent}</tr>\n'.format(indent=(self.tabs + 1) * 4 * ' ',
                                        key=key,
                                        content=content)
        return res

    def visit_dict(self, node):
        res = ''
        children = node.children.items()
        for key, child in children:
            res = self.visit_node(child, key, res)

        return '{indent}<table border="1"><caption>Object</caption><tbody>\n' \
               '{indent}    <tr><th>Name</th><th>Value</th></tr>\n' \
               '{content}' \
               '{indent}</tbody></table>\n'.format(indent=self.tabs * 4 * ' ',
                                                   content=res)

    def visit_list(self, node):
        res = ''
        children = node.children.items()
        for key, child in children:
            res = self.visit_node(child, key, res)

        return '{indent}<table border="2"><caption>List</caption><tbody>\n' \
               '{indent}    <tr><th>Index</th><th>Value</th></tr>\n' \
               '{content}' \
               '{indent}</tbody></table>\n'.format(indent=self.tabs * 4 * ' ',
                                                   content=res)

    def visit_base(self, node):
        return '{indent}{content}\n'.format(indent=self.tabs * 4 * ' ',
                                            content=node.val)



