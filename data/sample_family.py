from models.person import Person
from models.family_tree import FamilyTree
from music.music_generator import person_to_note


# create sample people
def create_sample_family():
    people = []

    bob = Person("Bob", 1960)
    jane = Person("Jane", 1962)
    alice = Person("Alice", 1985)
    summer = Person("Summer", 2000)
    ella = Person("Ella", 1999)
    logan = Person("Logan", 2007)
    kent = Person("Kent", 2025)
    mark = Person("Mark", 2000)
    bill = Person("Bill", 2050)
    carol = Person("Carol", 2007)
    jr = Person("Jr", 2034)
    mary = Person("Mary", 2024)

    # create sample family relationships
    bob.add_child(alice)
    bob.add_child(summer)
    alice.add_parent(jane)
    summer.add_parent(jane)
    alice.add_child(ella)
    alice.add_child(logan)
    ella.add_child(kent)
    kent.add_child(bill)
    mark.add_child(kent)
    logan.add_child(jr)
    carol.add_child(jr)
    bill.add_parent(mary)

    people.append(bob)
    people.append(alice)
    people.append(summer)
    people.append(ella)
    people.append(logan)
    people.append(kent)
    people.append(mark)
    people.append(bill)
    people.append(carol)
    people.append(jr)
    people.append(mary)
    people.append(jane)

    return people


family = create_sample_family()
tree = FamilyTree(family)