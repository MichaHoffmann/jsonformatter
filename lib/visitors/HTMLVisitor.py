from lib.visitors.JSONVisitor import JSONVisitor

class HTMLVisitor(JSONVisitor):
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
