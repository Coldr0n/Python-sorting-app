import pygame as pg

class DropDown(pg.sprite.Sprite):
    def __init__(self, element_rect, font, elements, *groups, color='white', bg_color='black', selected_element=0, callback=lambda x: None):
        super().__init__(*groups)
        self.element_size = element_rect.size
        self.rect = element_rect

        self.image = pg.Surface(self.element_size)
        self.image.fill(bg_color)

        self.font = font
        self.elements = elements
        self.color = color
        self.bg_color = bg_color
        self.selected_element = selected_element
        self.callback = callback

        self.collapsed = True
        self.draw_collapsed()

    def collapse(self):
        self.collapsed = True
        self.draw_collapsed()

    def select(self, pos):
        dy = pos[1] - self.rect.y
        selected_box = int(dy / self.element_size[1])
        if selected_box != 0:
            self.selected_element = selected_box - 1
            self.callback(self.elements[self.selected_element])

        self.collapsed = True
        self.draw_collapsed()

    def expand(self):
        self.collapsed = False
        self.draw_expanded()

    def draw_collapsed(self):
        self.rect.size = self.element_size
        self.image = pg.Surface(self.element_size)
        self.image.fill(self.bg_color)
        text_surf = self.font.render(self.elements[self.selected_element], True, self.color)
        text_rect = text_surf.get_rect(center=self.image.get_rect().center)

        self.image.blit(text_surf, text_rect)      

    def draw_expanded(self):
        self.rect.height = self.element_size[1] * (len(self.elements) + 1)
        self.image = pg.Surface(self.rect.size)
        self.image.fill(self.bg_color)

        pg.draw.rect(self.image, pg.Color(self.bg_color) - pg.Color('grey5'), ((0, self.element_size[1] * (self.selected_element + 1)), self.element_size))

        # Draw the selected element
        text_surf = self.font.render(self.elements[self.selected_element], True, self.color)
        text_rect = text_surf.get_rect(center=pg.Rect((0, 0), self.element_size).center)
        self.image.blit(text_surf, text_rect)

        for i in range(1, len(self.elements) + 1):
            text_surf = self.font.render(self.elements[i - 1], True, self.color)
            text_rect = text_surf.get_rect(center=pg.Rect((0, 0), self.element_size).center)
            text_rect.y += self.element_size[1] * i

            self.image.blit(text_surf, text_rect)