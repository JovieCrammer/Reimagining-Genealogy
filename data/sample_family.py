from models.person import Person
from models.family_tree import FamilyTree

# create sample people
bob = Person("Bob", 1970)
alice = Person("Alice", 1995)
summer = Person("Summer", 2003)
ella = Person("Ella", 2006)
logan = Person("Logan", 2011)

# create sample family relationships
bob.add_child(alice)
bob.add_child(summer)
alice.add_child(ella)
alice.add_child(logan)

root = FamilyTree(bob)
