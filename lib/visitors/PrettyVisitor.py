from termcolor import colored
from lib.visitors.JSONVisitor import JSONVisitor


class PrettyVisitor(JSONVisitor):
    TAB = 3 * ' '
    OBJTMPL = '{{\n' + \
              '{content}\n' + \
              '{tabs}}}'

    LISTTMPL = '[\n' + \
               '{content}\n' + \
               '{tabs}]'

    def __init__(self):
        self.tabs = 0

    def visit_node(self, node):
        self.tabs += 1
        res = node.accept(self)
        self.tabs -= 1
        return res

    def visit_base(self, node):
        val = node.val
        if isinstance(val, bool):
            return colored(val, 'yellow')
        elif isinstance(val, int):
            return colored(val, 'red')
        elif isinstance(val, str):
            return colored('"{}"'.format(val), 'white')
        elif val is None:
            return colored('null', 'cyan')
        else:
            return colored(val, 'blue')

    def visit_dict(self, node):
        content = ''
        for i, item in enumerate(node.children.items()):
            key, val = item
            content += '{tabs}"{key}": {val}'.format(
                tabs=(self.tabs+1) * self.TAB,
                key=colored(key, 'green'),
                val=self.visit_node(val))
            if i != len(node.children) - 1:
                content += ',\n'

        return self.OBJTMPL.format(
            tabs=self.tabs * self.TAB,
            content=content)

    def visit_list(self, node):
        content = ''
        for key, val in node.children.items():
            content += '{tabs}{val}'.format(
                tabs=(self.tabs+1) * self.TAB,
                val=self.visit_node(val))
            if key != len(node.children) - 1:
                content += ',\n'

        return self.LISTTMPL.format(
            tabs=self.tabs * self.TAB,
            content=content)
        return node
