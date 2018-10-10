from termcolor import colored
from lib.visitors.JSONVisitor import JSONVisitor


class PrettyVisitor(JSONVisitor):
    TAB = 3 * ' '
    OBJTMPL = '{{\n' + \
              '{content}\n' + \
              '{tabs}}}'
    OBJITEMTMPL = '{tabs}"{key}": {val}'

    LISTTMPL = '[\n' + \
               '{content}\n' + \
               '{tabs}]'
    LISTITEMTMPL = '{tabs}{val}'

    CLISTTMPL = '[{content}]'
    CLISTITEMTMPL = '{val}'
    COBJTMPL = '{{{content}}}'
    COBJITEMTMPL = '"{key}":{val}'

    def __init__(self, compact=False, color=True):
        self.tabs = 0
        self.compact = compact
        if compact:
            self.list_template = self.CLISTTMPL
            self.list_item_tmpl = self.CLISTITEMTMPL
            self.obj_template = self.COBJTMPL
            self.obj_item_tmpl = self.COBJITEMTMPL
        else:
            self.list_template = self.LISTTMPL
            self.list_item_tmpl = self.LISTITEMTMPL
            self.obj_template = self.OBJTMPL
            self.obj_item_tmpl = self.OBJITEMTMPL

        if color:
            self.bool_color = lambda val: colored(val, 'yellow')
            self.int_color = lambda val: colored(val, 'red')
            self.str_color = lambda val: colored('"{}"'.format(val), 'cyan')
            self.null_color = lambda val: colored(val, 'blue')
            self.unkown_color = lambda val: colored(val, 'white')
            self.key_color = lambda key: colored(key, 'green')
        else:
            def plain_color(val): return val
            self.bool_color = plain_color
            self.int_color = plain_color
            self.str_color = lambda val: '"{}"'.format(val)
            self.null_color = plain_color
            self.unkown_color = plain_color
            self.key_color = plain_color

    def visit_node(self, node):
        self.tabs += 1
        res = node.accept(self)
        self.tabs -= 1
        return res

    def visit_base(self, node):
        val = node.val
        if isinstance(val, bool):
            return self.bool_color(val)
        elif isinstance(val, int):
            return self.int_color(val)
        elif isinstance(val, str):
            return self.str_color(val)
        elif val is None:
            return self.null_color(val)
        else:
            return self.unkown_color(val)

    def visit_dict(self, node):
        if len(node.children.items()) == 0:
            return "{}"

        content = ''
        for i, item in enumerate(node.children.items()):
            key, val = item
            content += self.obj_item_tmpl.format(
                tabs=(self.tabs+1) * self.TAB,
                key=self.key_color(key),
                val=self.visit_node(val))
            if i != len(node.children) - 1:
                content += ','
                if not self.compact:
                    content += '\n'

        return self.obj_template.format(
            tabs=self.tabs * self.TAB,
            content=content)

    def visit_list(self, node):
        if len(node.children.items()) == 0:
            return "[]"

        content = ''
        for key, val in node.children.items():
            content += self.list_item_tmpl.format(
                tabs=(self.tabs+1) * self.TAB,
                val=self.visit_node(val))
            if key != len(node.children) - 1:
                content += ','
                if not self.compact:
                    content += '\n'

        return self.list_template.format(
            tabs=self.tabs * self.TAB,
            content=content)
