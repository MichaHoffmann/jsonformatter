from lib.visitors.JSONVisitor import JSONVisitor

class FlattenVisitor(JSONVisitor):
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

