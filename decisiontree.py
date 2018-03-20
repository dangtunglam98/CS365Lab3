class Node:
    def __init__(self,attr):
        self.attr = attr # attribute
        self.val = ""   # attribute value
        self.children = []

    def check_leaf(self):
        if len(self.children) == 0:
            return True
        return False

class Tree:
    def __init__(self, attr):
        self.root = Node(attr)
        self.size = 1

    def add_branch(self, branch):
        self.root.children.append(branch.root)
        self.size = self.size + branch.size
