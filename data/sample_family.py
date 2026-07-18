from models.person import Person
from models.family_tree import FamilyTree
from music.music_generator import person_to_note

# create sample people
bob = Person("Bob", 1970)
alice = Person("Alice", 1995)
summer = Person("Summer", 2003)
ella = Person("Ella", 2000)
logan = Person("Logan", 2011)
kent = Person("Kent", 2025)

# create sample family relationships
bob.add_child(alice)
bob.add_child(summer)
alice.add_child(ella)
alice.add_child(logan)
ella.add_child(kent)

root = FamilyTree(bob)

# test converting a person to a note
print(person_to_note(bob, 0))
print(person_to_note(alice, 1))
print(person_to_note(ella, 2))