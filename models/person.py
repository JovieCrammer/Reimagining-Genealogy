# model a person
class Person:
    def __init__(self, name, birth_year=None):
        self.name = name
        self.birth_year = birth_year
        self.parents = []
        self.children = []

    def add_child(self, child):
        self.children.append(child)

        if self not in child.parents:
            child.parents.append(self)

    def add_parent(self, parent):
        self.parents.append(parent)

        if self not in parent.children:
            parent.children.append(self)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Person(name={self.name}, birth_year={self.birth_year}"
