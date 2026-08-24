import pygame


class InformationPanel:

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

    def draw(self, screen, person):
        if person is None:
            return

        panel_width = 320
        panel_height = 500

        panel_x = self.WIDTH - panel_width - 30
        panel_y = 30

        # panel background
        panel = pygame.Rect(
            panel_x,
            panel_y,
            panel_width,
            panel_height
        )

        pygame.draw.rect(
            screen,
            (18, 18, 18),
            panel,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            panel,
            width=1,
            border_radius=12
        )

        # fonts
        title_font = pygame.font.Font(None, 32)
        heading_font = pygame.font.Font(None, 22)
        body_font = pygame.font.Font(None, 20)

        x = panel_x + 25
        y = panel_y + 25

        # name
        title = title_font.render(
            person.name,
            True,
            (255, 255, 255)
        )

        screen.blit(title, (x, y))
        y += 45

        # information
        if person.birth_year is not None:
            text = body_font.render(
                f"Born: {person.birth_year}",
                True,
                (210, 210, 210)
            )
            screen.blit(text, (x, y))
            y += 28

        # parents
        heading = heading_font.render(
            "Parents",
            True,
            (255, 255, 255)
        )

        screen.blit(
            heading,
            (x, y)
        )
        y += 25

        if person.parents:
            for parent in person.parents:
                text = body_font.render(
                    f"• {parent.name}",
                    True,
                    (190, 190, 190)
                )

                screen.blit(
                    text,
                    (x + 5, y)
                )
                y += 23

        else:

            text = body_font.render(
                "Unknown",
                True,
                (120, 120, 120)
            )

            screen.blit(
                text,
                (x + 5, y)
            )

            y += 23
        y += 12

        # partner/s
        heading = heading_font.render(
            "Partner",
            True,
            (255, 255, 255)
        )

        screen.blit(heading, (x, y))
        y += 25

        partners = self.get_partners(person)
        if partners:

            for partner in partners:
                text = body_font.render(
                    f"• {partner.name}",
                    True,
                    (190, 190, 190)
                )

                screen.blit(text, (x + 5, y))
                y += 23

        else:
            text = body_font.render(
                "None recorded",
                True,
                (120, 120, 120)
            )

            screen.blit(text, (x + 5, y))
            y += 23
        y += 12

        # children
        heading = heading_font.render(
            "Children",
            True,
            (255, 255, 255)
        )

        screen.blit(heading, (x, y))
        y += 25

        if person.children:
            for child in person.children:
                text = body_font.render(
                    f"• {child.name}",
                    True,
                    (190, 190, 190)
                )

                screen.blit(text, (x + 5, y))
                y += 23

        else:
            text = body_font.render(
                "None recorded",
                True,
                (120, 120, 120)
            )

            screen.blit(text, (x + 5, y))

    @staticmethod
    def get_partners(person):
        partners = []
        for child in person.children:
            for parent in child.parents:
                if parent != person and parent not in partners:
                    partners.append(parent)

        return partners
