from random import shuffle

import pygame as pg

from button import Button
from pg_input import Input
from dropdown import DropDown
import sorting_generators

class App:
    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((1200, 800))

        self.nav_height = self.screen.get_height() // (len(sorting_generators.__all__) + 1)
        self.font = pg.font.SysFont('Arial', 20)

        self.buttons = pg.sprite.Group()
        Button(pg.Rect(0, 0, 100, self.nav_height), "Shuffle", self.font, 'White', (222, 69, 69), self.shuffle_array, self.buttons)
        Button(pg.Rect(105, 0, 100, self.nav_height), "Sort", self.font, 'White', (74, 222, 69), self.start_sort, self.buttons)

        self.inputs = pg.sprite.Group()
        Input(pg.Rect(210, 0, 100, self.nav_height), self.font, 'white', (51, 51, 51), self.init_array, self.inputs, max_char=4, numerical=True, text="100")
        Input(pg.Rect(315, 0, 100, self.nav_height), self.font, 'white', (51, 51, 51), self.set_delay, self.inputs, max_char=4, numerical=True, text="0")

        self.dropdowns = pg.sprite.Group()
        DropDown(pg.Rect(420, 0, 200, self.nav_height), self.font, sorting_generators.__all__, self.dropdowns, color='white', bg_color=(51, 51, 51), callback=self.change_algorithm)

        self.sort_surf = pg.Surface((self.screen.get_width(), self.screen.get_height() - self.nav_height))
        self.column_width = 0
        self.add_padding = True
        self.array = []
        self.swapped_indices = ()
        self.init_array(100)

        self.sorting_generator = sorting_generators.bubbleSort
        self.sort = self.sorting_generator(self.array)

        self.sorting = False
        self.delay = 0
        self.running = True

    def change_algorithm(self, alg):
        self.sorting_generator = getattr(sorting_generators, alg)

    def set_delay(self, delay):
        self.delay = delay

    def start_sort(self):
        self.sorting = True
        self.sort = self.sorting_generator(self.array)

    def init_array(self, length):
        self.sorting = False
        self.swapped_indices = ()
        self.array = list(range(1, length + 1))
        if length != 0:
            self.add_padding = length <= self.sort_surf.get_width() // 2
            self.column_width = (self.sort_surf.get_width() - (length if self.add_padding else 0)) / length

    def shuffle_array(self):
        self.sorting = False
        self.swapped_indices = ()
        shuffle(self.array)

    def handle_inputs(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        button.click()

                for input in self.inputs:
                    input.set_focus(input.rect.collidepoint(event.pos))

                for dropdown in self.dropdowns:
                    if dropdown.rect.collidepoint(event.pos):
                        if dropdown.collapsed:
                            dropdown.expand()
                        else:
                            dropdown.select(event.pos)
                    else:
                        dropdown.collapse()

            if event.type == pg.KEYDOWN:
                for input in self.inputs:
                    if input.focus:
                        if event.key == pg.K_BACKSPACE:
                            input.remove_char()
                        elif event.key == pg.K_RETURN:
                            input.call()
                        else:
                            input.add_char(event.unicode)
                        break

    def update(self):
        if self.sorting:
            try:
                self.array, self.swapped_indices = next(self.sort)
                pg.time.delay(self.delay)
            except StopIteration:
                self.sorting = False

    def draw_array(self):
        self.sort_surf.fill('black')
        line_rect = pg.Rect(0, 0, 0, 0)
        line_rect.width = self.column_width
        for i in range(len(self.array)):
            line_rect.x = i * self.column_width + (i if self.add_padding else 0)
            line_rect.height = self.array[i] / len(self.array) * self.sort_surf.get_height()
            line_rect.y = self.sort_surf.get_height() - line_rect.h
            color = 'green' if i in self.swapped_indices else 'white'
            pg.draw.rect(self.sort_surf, color, line_rect)

        self.screen.blit(self.sort_surf, (0, self.screen.get_height() - self.sort_surf.get_height()))

    def draw(self):
        self.screen.fill('BLACK')
        self.draw_array()
        pg.draw.line(self.screen, 'GREY', (0, self.nav_height), (self.screen.get_width(), self.nav_height))
        
        self.buttons.draw(self.screen)
        self.inputs.draw(self.screen)
        self.dropdowns.draw(self.screen)
        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_inputs()
            self.update()
            self.draw()

        pg.quit()

if __name__ == '__main__':
    app = App()
    app.run()
