import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, rect: pg.Rect, text, font: pg.font.Font, color='white', bg_color='black', callback=lambda: None, *groups):
        super().__init__(*groups)
        self.rect = rect

        self.image = pg.Surface(rect.size)
        self.image.fill(bg_color)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
            
        self.image.blit(text_surface, text_rect)

        self.callback = callback

    def click(self):
        self.callback()