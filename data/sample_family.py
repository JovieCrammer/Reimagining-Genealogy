from models.person import Person
from models.family_tree import FamilyTree
from music.music_generator import person_to_note

# create sample people
bob = Person("Bob", 1960)
alice = Person("Alice", 1985)
summer = Person("Summer", 2000)
ella = Person("Ella", 1999)
logan = Person("Logan", 2007)
kent = Person("Kent", 2025)
mark = Person("Mark", 2000)
bill = Person("Bill", 2050)

# create sample family relationships
bob.add_child(alice)
bob.add_child(summer)
alice.add_child(ella)
alice.add_child(logan)
ella.add_child(kent)
kent.add_child(bill)

root = FamilyTree(bob)

# test converting a person to a note
print(kent.parents)