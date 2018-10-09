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

