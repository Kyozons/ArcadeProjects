#!/usr/bin/env python3

import arcade

# --- Constantes ---
BACKGROUND_COLOR = arcade.color.AMAZON
SCREEN_WIDHT = 800
SCREEN_HEIGHT = 600
TITLE = "Sprite and Walls"

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_BOX = 0.5

MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    """ Clase Window custom"""
    def __init__(self):
        """ Inicializador """
        # Llama a la clase init del padre
        super().__init__(SCREEN_WIDHT, SCREEN_HEIGHT, TITLE)

        # Lista de Sprites
        self.player_list = None
        self.wall_list = None

        # Jugador
        self.player_sprite = None

        # Motor de fisicas
        self.physics_engine = None

        # Crear Cámaras, una para la GUI
        # Y la otra para los Sprites
        self.camera_for_sprites = arcade.Camera(SCREEN_WIDHT, SCREEN_HEIGHT)
        self.camera_for_gui = arcade.Camera(SCREEN_WIDHT, SCREEN_HEIGHT)

    def setup(self):
        """ Preparar el juego e inicializar las variables"""

        # Color de fondo
        arcade.set_background_color(BACKGROUND_COLOR)

        # Inicializar Lista de Sprites
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Puntaje
        self.score = 0

        # Crear Jugador
        self.player_sprite = arcade.Sprite("../Assets/Sprites/character.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)

        # Crear y poscisionar caja en 300, 200
        wall = arcade.Sprite("../Assets/Sprites/box.png", SPRITE_SCALING_BOX)
        wall.center_x = 300
        wall.center_y = 200
        self.wall_list.append(wall)

        # Crear y poscisionar caja en 364, 200
        wall = arcade.Sprite("../Assets/Sprites/box.png", SPRITE_SCALING_BOX)
        wall.center_x = 364
        wall.center_y = 200
        self.wall_list.append(wall)

        # Crear y poscisionar cajas en un loop
        for x in range(173, 650, 64):  # Cambiar el valor desde 173 a 650, cada 64 pixels
            wall = arcade.Sprite("../Assets/Sprites/box.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 350  # El eje Y es constante ya que queremos hacer una plataforma
            self.wall_list.append(wall)

        # Crear y poscisionar cajas en base a una lista
        coordinate_list = [[400, 500], [470, 500], [400, 570], [470, 570]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("../Assets/Sprites/box.png", SPRITE_SCALING_BOX)
            wall.center_x = coordinate[0]
            wall.center_y = coordinate[1]
            self.wall_list.append(wall)

        # Motor de Físicas
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


    def on_draw(self):
        arcade.start_render()

        # Selecciona la cámara que va a moverse para los sprites
        self.camera_for_sprites.use()

        # Dibujar los Sprites
        self.wall_list.draw()
        self.player_list.draw()

        # Selecciona la cámara FIJA para la GUI
        self.camera_for_gui.use()
        arcade.draw_text(f"Puntaje: {self.score}", 10, 10, arcade.color.WHITE, 24)

    def on_update(self, delta_time):
        """ Movimiento y lógica del juego"""

        # Actualiza todos los sprite
        self.physics_engine.update()


        # Mueve la ventana al jugador
        #
        # Si CAMERA_SPEED es 1, la camara se moverá inmediatamente a la poscision deseada
        # Cualquier número entre 0 y 1 hará que la cámara se mueva en una manera más suave
        CAMERA_SPEED = 1
        lower_left_corner = (self.player_sprite.center_x - self.width / 2, self.player_sprite.center_y - self.height / 2)
        self.camera_for_sprites.move_to(lower_left_corner, CAMERA_SPEED)

    def on_key_press(self, key, modifiers):
        """ Se llama cada vez que se presiona una tecla"""

        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        """ Se llama cuando se suelta una tecla"""

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

def main():
    """ Metodo principal"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
