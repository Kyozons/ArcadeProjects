#!/usr/bin/env python3

import arcade

# --- CONSTANTES ---

# Cuantas filas y columnas
ROW_COUNT = 10
COLUMN_COUNT = 10

# Definir el ancho y alto de cada casilla
WIDTH = 20
HEIGHT = 20

# Margen entre cada celda y a los bordes de la pantalla
MARGIN = 5

# Dimensiones de la pantalla en base a los valores anteriores
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


class MyGame(arcade.Window):
    """
    Clase principal
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        # Crear un array de dos dimensiones
        self.grid = []
        for row in range(ROW_COUNT):
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)
        # Crear un array de dos dimensiones con list comprehention
        self.grid = [[0 for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """
        Renderizar la pantalla
        """
        arcade.start_render()

        # Dibujar la rejilla
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Decidir de qué color pintar la celda
                if self.grid[row][column] == 1:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.WHITE

                # Calcular donde posicionar las celdas
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Dibuja las celdas
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Se llama cuando se presiona un boton del mouse
        """

        # Cambia las coordenadas de x/y para coordenadas de celda
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)


        # Asegurarse de que se haga click dentro de la rejilla ya que se puede
        # hacer click en las esquinas donde corresponde margen y no corresponde
        # una coordenada de celda
        if row < ROW_COUNT and column < COLUMN_COUNT:
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
            else:
                self.grid[row][column] = 0
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()
