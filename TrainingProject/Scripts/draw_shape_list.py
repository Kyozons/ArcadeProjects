#!/usr/bin/env python3

import arcade
import timeit

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Dibujar con lista de formas"

SQUARE_WIDTH = 5
SQUARE_HEIGHT = 5
SQUARE_SPACING = 10


class MyGame(arcade.Window):
    """ clase principal de la app"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.draw_time = 0
        self.shape_list = None

    def setup(self):
        # Crear la lista de formas antes de dibujar
        self.shape_list = arcade.ShapeElementList()
        for x in range(0, SCREEN_WIDTH, SQUARE_SPACING):
            for y in range(0, SCREEN_HEIGHT, SQUARE_SPACING):
                shape = arcade.create_rectangle_filled(x, y, SQUARE_WIDTH, SQUARE_HEIGHT, arcade.color.DARK_BLUE)
                self.shape_list.append(shape)


    def on_draw(self):
        """ Renderizar la pantalla"""

        # Éste comando tiene que pasar antes de comenzar a dibujar
        self.clear()

        # Cronometrar cuanto se demora
        draw_start_time = timeit.default_timer()

        # --- Dibujar toods los rectangulos
        self.shape_list.draw()

        # Print el tiempo que demora
        output = f"Tiempo de dibujado: {self.draw_time:.3f} segundos por fotograma."
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18)

        self.draw_time = timeit.default_timer() - draw_start_time

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
