#!/usr/bin/env python3

import arcade
import random

# --- Constantes ---
SCREEN_WIDHT = 800
SCREEN_HEIGHT = 600
TITLE = "Colisiones Y Sprites"

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 18

class Coin(arcade.Sprite):

    """
    Esta clase representa las monedas en la pantalla.
    Es una clase Hija de la clase "Sprite" de la
    libreria Arcade
    """

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    # def reset_pos(self):
    #         # Resetea la posición en un lugar aleatoreo en la parte superior de la pantalla
    #         self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
    #         self.center_x = random.randrange(SCREEN_WIDHT)

    def update(self):

        # Mover la moneda
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Ver si la moneda se cae al fondo de la pantalla
        # Si lo hace, resetear su posición
        # if self.top < 0:
            # self.reset_pos()

        # Rotar el sprite
        self.angle += 1

        # Si rotamos más de 360, resetea el angulo
        if self.angle > 359:
            self.angle -= 360


        # Si estamos "fuera del limite", rebota
        if self.left < 0:
            self.change_x *= -1
        if self.right > SCREEN_WIDHT:
            self.change_x *= -1
        if self.bottom < 0:
            self.change_y *= -1
        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1



class MyGame(arcade.Window):
    """ Clase Window custom"""
    def __init__(self):
        """ Inicializador """
        # Llama a la clase init del padre
        super().__init__(SCREEN_WIDHT, SCREEN_HEIGHT, TITLE)

        # Variables para las listas de sprites
        self.player_list = None
        self.coin_list = None

        # Preparar info del jugador
        self.player_sprite = None
        self.score = 0

        # Ocultar el cursor del  mouse
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Preparar el juego e inicializar las variables"""

        # Lista de Sprites
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Puntaje
        self.score = 0

        # Preparar al jugador
        self.player_sprite = arcade.Sprite("../Assets/Sprites/character.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Crear los Coins
        for i in range(COIN_COUNT):

            # Crear el instance del coin
            coin = Coin("../Assets/Sprites/coin_01.png", SPRITE_SCALING_COIN)

            # Posicionar el Coin
            coin.center_x = 400
            coin.center_y = random.randrange(10, SCREEN_HEIGHT -10)
            coin.change_x = random.choice((-1,1))
            coin.change_y = 0

            # Añade el coin a la lista
            self.coin_list.append(coin)

    def on_draw(self):
        arcade.start_render()

        """ Aqui se dibujan las listas de sprites.
        Por lo general los sprites se dividen en
        grupos diferentes. Los sprites que no se
        mueven se debrian dibujar en su propio
        grupo para obtener el mejor rendimiento
        Se debe intentar evitar dibujar sprites
        solos, es mejor usar una SpriteList
        ya que dentro de ese metodo hay mejoras
        al rendimiento"""

        self.coin_list.draw()
        self.player_list.draw()

        # Mostrar puntaje en pantalla
        output = f"Puntos: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):

        """ Se encarga del movimiento del mouse"""

        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movimiento y lógica del juego"""

        # Actualizar toda la lista de sprites
        self.coin_list.update()

        # Una lista de todas los sprites que colisionen con el jugador
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)

        # Loop por cada sprite que colisione, reinicia su poscision y añade +1 al score
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

def main():
    """ Metodo principal"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
