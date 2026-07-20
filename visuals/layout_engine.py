class LayoutEngine:
    def __init__(self, tree, width, height):
        self.tree = tree
        self.width = width
        self.height = height
        self.horizontal = 150
        self.vertical = 120

    def layout(self):
        layers = self.layer()
        ordered_layers = self.order_layers(layers)
        positions = self.position(ordered_layers)
        return positions

    def layer(self):
        return self.tree.get_generations()

    @staticmethod
    def order_layers(layers):
        return layers

    def position(self, ordered_layers):
        positions = {}
        for generation, people in enumerate(ordered_layers):
            y = 100 + generation * self.vertical
            count = len(people)
            if count == 0:
                continue
            total_width = (count - 1) * self.horizontal
            centre = self.width / 2
            start_x = centre - total_width / 2

            for i, person in enumerate(people):
                x = start_x + i * self.horizontal
                positions[person] = (x, y)
        return positions
