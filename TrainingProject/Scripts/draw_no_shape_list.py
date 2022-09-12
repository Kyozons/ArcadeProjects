#!/usr/bin/env python3

import arcade
import timeit

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Demo con lista de formas"

SQUARE_WIDTH = 5
SQUARE_HEIGHT = 5
SQUARE_SPACING = 10


class MyGame(arcade.Window):
    """ clase principal de la app"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.draw_time = 0

    def on_draw(self):
        """ Renderizar la pantalla"""

        # Éste comando tiene que pasar antes de comenzar a dibujar
        self.clear()

        # Cronometrar cuanto se demora
        draw_start_time = timeit.default_timer()

        # --- Dibujar toods los rectangulos
        for x in range (0, SCREEN_WIDTH, SQUARE_SPACING):
            for y in range(0, SCREEN_HEIGHT, SQUARE_SPACING):
                arcade.draw_rectangle_filled(x, y, SQUARE_WIDTH, SQUARE_HEIGHT, arcade.color.DARK_BLUE)

        # Print el tiempo que demora
        output = f"Tiempo de dibujado: {self.draw_time:.3f} segundos por fotograma."
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18)

        self.draw_time = timeit.default_timer() - draw_start_time

def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.run()

if __name__ == "__main__":
    main()
