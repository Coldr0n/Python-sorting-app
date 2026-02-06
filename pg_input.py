import pygame as pg


class TextInput(pg.sprite.Sprite):
    def __init__(
        self,
        rect,
        font,
        color="white",
        bg_color="black",
        callback=lambda: None,
        *groups,
        max_char=30,
        numerical=False,
        text=""
    ):
        super().__init__(*groups)
        self.rect = rect

        self.image = pg.Surface(rect.size)
        self.image.fill(bg_color)

        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.max_char = max_char
        self.callback = callback
        self.numerical = numerical

        self.focus = False
        self.text: str = ""
        self.set_text(text)

    def set_focus(self, focus):
        self.focus = focus
        self.update_image()

    def call(self):
        self.callback(int(self.text) if self.numerical else self.text)
        self.set_focus(False)

    def set_text(self, text: str):
        if len(text) <= self.max_char:
            if (not self.numerical and text.isalnum()) or (
                self.numerical and text.isnumeric()
            ):
                self.text = text
                self.update_image()

    def add_char(self, character: str):
        self.set_text(self.text + character)

    def remove_char(self):
        self.text = self.text[:-1]
        self.update_image()

    def update_image(self):
        bg_color = (
            pg.Color(self.bg_color) - pg.Color("grey5") if self.focus else self.bg_color
        )
        self.image.fill(bg_color)
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.image.get_rect().center)

        self.image.blit(text_surf, text_rect)
