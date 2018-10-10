from lib.visitors.JSONVisitor import JSONVisitor


class PathVisitor(object):
    def __init__(self, path_string):
        self.path = self.parse_path(path_string)

    @staticmethod
    def parse_path(path_string):
        res = []
        chars = list(reversed(path_string))
        cur_key = ''
        while chars:
            c = chars.pop()
            if c == '.':
                res.append(cur_key.strip('"'))
                cur_key = ''
            elif c == '[':
                res.append(cur_key.strip('"'))
                cur_key = '['
                depth = 1
                while depth > 0:
                    c = chars.pop()
                    if c == '[':
                        depth += 1
                    if c == ']':
                        depth -= 1
                    cur_key += c
                cur_key = cur_key[1:-1]
            else:
                cur_key += c

        if cur_key != '':
            res.append(cur_key.strip('"'))

        return res

    def visit_base(self, node):
        return node

    def visit_list(self, node):
        index = int(self.path[0])
        if len(self.path) == 1:
            return node.children[index]

        self.path = self.path[1:]
        return node.children[index].accept(self)

    def visit_dict(self, node):
        key = self.path[0]
        if len(self.path) == 1:
            return node.children[key]

        self.path = self.path[1:]
        return node.children[key].accept(self)
