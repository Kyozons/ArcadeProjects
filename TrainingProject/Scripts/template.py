#!/usr/bin/env python3

import arcade

# --- Constantes ---

SPRITE_SCALING = 0.5

# --- Rutas de archivos ---
ROUTE_SPRITES = "../Assets/Sprites"
PLAYER_SPRITE_NAME = "character.png"
WALL_SPRITE_NAME = "box.png"
COIN_SPRITE_NAME = "coin_01.png"

# --- Parametros del juego ---
BACKGROUND_COLOR = arcade.color.AMAZON
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
TITLE = "Template"
PLAYER_MOVEMENT_SPEED = 5
PLAYER_INITIAL_POS_X = 300
PLAYER_INITIAL_POS_Y = 300

# --- Control de Cámara ---

# Márgen de cuántos pixel mínimo mantener entre el personaje y el borde de la pantalla
VIEWPOINT_MARGIN = 200

# Velocidad en que la cámara persigue al jugador, 1 es instantáneo
CAMERA_SPEED = 0.1

class MyGame(arcade.Window):
    """ Clase Window custom"""
    def __init__(self):
        """ Inicializador """
        # Llama a la clase init del padre
        super().__init__(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, TITLE)

        # Lista de Sprites
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        # Preparar al jugador
        self.player_sprite = None
        self.physics_engine = None

        # Variable para manejar el puntaje
        self.score = 0

        # Se usan para manejar el scroll de camara
        self.view_bottom = 0
        self.view_left = 0

        # Llevar seguimiento de las teclas persionadas
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    def setup(self):
        """ Preparar el juego e inicializar las variables"""

        # Color de fondo
        arcade.set_background_color(BACKGROUND_COLOR)

        # Lista de Sprite
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()


        # Preparar al jugador
        self.player_sprite = arcade.Sprite(f"{ROUTE_SPRITES}/{PLAYER_SPRITE_NAME}", SPRITE_SCALING)
        self.player_sprite.center_x = PLAYER_INITIAL_POS_X
        self.player_sprite.center_y = PLAYER_INITIAL_POS_Y
        self.player_list.append(self.player_sprite)

        # Preparar Assets o murallas
        wall = arcade.Sprite(f"{ROUTE_SPRITES}/{WALL_SPRITE_NAME}", SPRITE_SCALING)
        wall.center_x = 250
        wall.center_y = 550
        self.wall_list.append(wall)

        coin = arcade.Sprite(f"{ROUTE_SPRITES}/{COIN_SPRITE_NAME}", SPRITE_SCALING / 2)
        coin.center_x = 300
        coin.center_y = 200
        self.coin_list.append(coin)

        # Elegir el motor de físicas a usar
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)  # arcade.PhysicsEngine

        # Setear los límites de la vista
        # Éstos parámetros indicar hacia donde hemos "scrolleado"
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """ Dibujar en pantalla"""

        # Éste comando debe pasar antes de comenzar a dibujar
        self.clear()

        # Seleccionar cámara donde dibujar los sprites
        self.camera_sprites.use()

        # Dibujar Sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

        # Dibujar el puntaje
        output = f"Puntaje: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        # Seleccionar la cámara inmóvil para GUI
        self.camera_gui.use()

        # Dibujar la GUI
        # ... TODO


    def on_key_press(self, key, modifiers):
        """ Se llama cada vez que se presiona una tecla"""

        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        """ Se llama cuando se suelta una tecla"""
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movimiento y lógica del juego"""

        # Calcular la velocidad en base a las teclas presionadas
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Ver si el player choca con una moneda
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        # Revisar lista de hits y eliminar de la lista cada moneda chocada, y sumar 1 al puntaje
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Actualizar todos los sprites
        self.physics_engine.update()

        # Mover la pantalla al jugador
        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Mueve la pantalla al jugador
        Éste método intentará mantener al jugador al menos a
        VIEWPORT_MARGIN pixel de distancia del borde

        Si CAMERA_SPEED es 1, la cámara se moverá inmediatamente
        a la poscisión deseada. Cualquier valor entre 0 y 1
        hará que la cámara se mueva de manera más fluida
        """

        # --- Controlar el Scroll ---

        # Hacia la izquierda
        left_boundary = self.view_left + VIEWPOINT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left

        # Hacia la derecha
        right_boundary = self.view_left + self.width - VIEWPOINT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary

        # Hacia Arriba
        top_boundary = self.view_bottom + self.height - VIEWPOINT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - self.player_sprite.bottom

        # Hacia Abajo
        bottom_boundary = self.view_bottom + VIEWPOINT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom

        # Scrollear a la ubicación correcta
        position = self.view_left, self.view_bottom
        self.camera_sprites.move_to(position, CAMERA_SPEED)


    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))




def main():
    """ Metodo principal"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
