from abc import ABCMeta, abstractmethod
import json
from collections import OrderedDict

from JSONVistor import JSONHtmlVisitor, JSONFlattenVisitor


class JSONTree(object):
    __meta__ = ABCMeta

    def __init__(self, val):
        self.children = OrderedDict()
        self.parse(val)

    @staticmethod
    def from_string(json_string):
        d = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(json_string)
        return JSONTree.get_node(d)

    @staticmethod
    def get_node(val):
        if isinstance(val, dict):
            return JSONDictNode(val)
        elif isinstance(val, list):
            return JSONListNode(val)
        else:
            return JSONBaseNode(val)

    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def parse(self, val):
        pass

    def htmlize(self):
        return self.accept(JSONHtmlVisitor())

    def flatten(self):
        return self.accept(JSONFlattenVisitor())


class JSONDictNode(JSONTree):
    def parse(self, json_dict):
        for key, val in json_dict.items():
            self.children[key] = self.get_node(val)

    def accept(self, visitor):
        return visitor.visit_dict(self)


class JSONListNode(JSONTree):
    def parse(self, json_list):
        for index, val in enumerate(json_list):
            self.children[index] = self.get_node(val)

    def accept(self, visitor):
        return visitor.visit_list(self)


class JSONBaseNode(JSONTree):
    def __init__(self, val):
        super(JSONBaseNode, self).__init__(val)
        self.val = val

    def parse(self, val):
        pass

    def accept(self, visitor):
        return visitor.visit_base(self)


