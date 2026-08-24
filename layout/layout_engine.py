class LayoutEngine:

    def __init__(self, tree, width, height):
        self.tree = tree
        self.width = width
        self.height = height

        # vertical distance between family levels
        self.vertical = 130

        # distance between partners
        self.partner_spacing = 75

        # minimum distance between separate family units
        self.family_spacing = 100

    def layout(self):

        people = self.tree.get_all_people()

        # if two people share a child, they are the same family unit
        parent = {
            person: person
            for person in people
        }

        def find(person):
            while parent[person] != person:
                parent[person] = parent[parent[person]]
                person = parent[person]

            return person

        def union(a, b):

            root_a = find(a)
            root_b = find(b)

            if root_a != root_b:
                parent[root_b] = root_a

        # people who share a child become partners
        for child in people:

            if len(child.parents) < 2:
                continue

            first_parent = child.parents[0]

            for other_parent in child.parents[1:]:
                union(first_parent, other_parent)

        units = {}

        for person in people:

            root = find(person)

            if root not in units:
                units[root] = []

            units[root].append(person)

        units = list(units.values())

        # map person -> family unit
        person_to_unit = {}

        for unit in units:
            for person in unit:
                person_to_unit[person] = unit

        unit_parents = {
            id(unit): set()
            for unit in units
        }

        unit_children = {
            id(unit): set()
            for unit in units
        }

        for child in people:

            child_unit = person_to_unit[child]

            for person_parent in child.parents:

                parent_unit = person_to_unit[person_parent]

                if parent_unit is child_unit:
                    continue

                unit_children[id(parent_unit)].add(
                    id(child_unit)
                )

                unit_parents[id(child_unit)].add(
                    id(parent_unit)
                )

        unit_lookup = {
            id(unit): unit
            for unit in units
        }

        levels = {
            id(unit): 0
            for unit in units
        }

        changed = True

        while changed:

            changed = False

            for unit in units:

                unit_id = id(unit)

                for child_id in unit_children[unit_id]:

                    new_level = levels[unit_id] + 1

                    if levels[child_id] < new_level:

                        levels[child_id] = new_level
                        changed = True

        levels_dict = {}

        for unit in units:

            level = levels[id(unit)]

            if level not in levels_dict:
                levels_dict[level] = []

            levels_dict[level].append(unit)

        positions = {}
        unit_centres = {}

        max_level = max(levels_dict.keys())

        for level in range(max_level + 1):

            current_units = levels_dict.get(level, [])

            if not current_units:
                continue

            desired = []

            for unit in current_units:

                parent_centres = []

                for parent_id in unit_parents[id(unit)]:

                    if parent_id in unit_centres:
                        parent_centres.append(
                            unit_centres[parent_id]
                        )

                if parent_centres:

                    desired_x = sum(parent_centres) / len(
                        parent_centres
                    )

                else:

                    desired_x = self.width / 2

                desired.append(
                    (unit, desired_x)
                )

            desired.sort(
                key=lambda item: item[1]
            )

            placed = []

            for unit, desired_x in desired:

                unit_width = (
                    (len(unit) - 1)
                    * self.partner_spacing
                )

                half_width = unit_width / 2

                x = desired_x

                if placed:

                    previous_unit, previous_x = placed[-1]

                    previous_width = (
                        (len(previous_unit) - 1)
                        * self.partner_spacing
                    )

                    minimum_x = (
                        previous_x
                        + previous_width / 2
                        + self.family_spacing
                        + half_width
                    )

                    x = max(x, minimum_x)

                placed.append(
                    (unit, x)
                )

            if placed:

                first_unit, first_x = placed[0]
                last_unit, last_x = placed[-1]

                first_width = (
                    (len(first_unit) - 1)
                    * self.partner_spacing
                )

                last_width = (
                    (len(last_unit) - 1)
                    * self.partner_spacing
                )

                left = first_x - first_width / 2
                right = last_x + last_width / 2

                row_centre = (left + right) / 2

                offset = (
                    self.width / 2
                    - row_centre
                )

            else:
                offset = 0

            for unit, centre_x in placed:

                centre_x += offset

                unit_centres[id(unit)] = centre_x

                unit_y = 100 + level * self.vertical

                unit_people = sorted(
                    unit,
                    key=lambda person: (
                        person.birth_year
                        if person.birth_year is not None
                        else 999999
                    )
                )

                total_width = (
                    (len(unit_people) - 1)
                    * self.partner_spacing
                )

                start_x = (
                    centre_x
                    - total_width / 2
                )

                for i, person in enumerate(unit_people):

                    positions[person] = (
                        start_x
                        + i * self.partner_spacing,
                        unit_y
                    )
        return positions
