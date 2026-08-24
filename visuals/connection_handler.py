import pygame


class ConnectionHandler:
    def __init__(self, camera, node_dictionary):
        self.camera = camera
        self. node_dictionary = node_dictionary

    def draw(self, screen, people):

        drawn_couples = set()
        for person in people:

            # 1. draw partner (horizontal lines)
            if len(person.parents) >= 2:
                parents = tuple(
                    sorted(
                        person.parents,
                        key=lambda p: p.name
                    )
                )

                if parents not in drawn_couples:

                    # only draw if both parents are visible
                    if all(
                            self.node_dictionary[parent].visible
                            for parent in parents
                    ):
                        parent_nodes = [
                            self.node_dictionary[parent]
                            for parent in parents
                        ]

                        parent_positions = [
                            self.camera.world_to_screen(
                                (node.x, node.y)
                            )
                            for node in parent_nodes
                        ]

                        pygame.draw.line(
                            screen,
                            "grey18",
                            parent_positions[0],
                            parent_positions[1],
                            1
                        )

                        drawn_couples.add(parents)

            # 2. draw child connection
            if not person.parents:
                continue

            child_node = self.node_dictionary[person]

            if not child_node.visible:
                continue

            parent_nodes = [
                self.node_dictionary[parent]
                for parent in person.parents
                if self.node_dictionary[parent].visible
            ]

            if not parent_nodes:
                continue

            # midpoint between the parents
            if len(parent_nodes) >= 2:

                parent_positions = [
                    self.camera.world_to_screen(
                        (node.x, node.y)
                    )
                    for node in parent_nodes
                ]

                parent_x = sum(
                    position[0]
                    for position in parent_positions
                ) / len(parent_positions)

                parent_y = sum(
                    position[1]
                    for position in parent_positions
                ) / len(parent_positions)

                parent_centre = (
                    parent_x,
                    parent_y
                )

                child_position = self.camera.world_to_screen(
                    (child_node.x, child_node.y)
                )

                pygame.draw.line(
                    screen,
                    "grey18",
                    parent_centre,
                    child_position,
                    1
                )

            # if there is only one parent connect directly
            else:

                parent_node = parent_nodes[0]

                parent_position = self.camera.world_to_screen(
                    (parent_node.x, parent_node.y)
                )

                child_position = self.camera.world_to_screen(
                    (child_node.x, child_node.y)
                )

                pygame.draw.line(
                    screen,
                    "grey18",
                    parent_position,
                    child_position,
                    1
                )