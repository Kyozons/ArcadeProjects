#!/usr/bin/env python3

import arcade
import setup_rooms as stp

# --- Constantes ---

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

# --- Rutas de archivos ---
ROUTE_SPRITES = "../../Assets/Sprites"
PLAYER_SPRITE_NAME = "character.png"
WALL_SPRITE_NAME = "box.png"
COIN_SPRITE_NAME = "coin_01.png"

# --- Parametros del juego ---
BACKGROUND_COLOR = arcade.color.AMAZON
SCREEN_WIDTH = SPRITE_SIZE * 14
SCREEN_HEIGHT = SPRITE_SIZE * 10
TITLE = "Moverse por habitaciones"
PLAYER_MOVEMENT_SPEED = 5
PLAYER_INITIAL_POS_X = 100
PLAYER_INITIAL_POS_Y = 100


class MyGame(arcade.Window):
    """ Clase Window custom"""
    def __init__(self):
        """ Inicializador """
        # Llama a la clase init del padre
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)

        # Rooms
        self.current_room = 0

        # Lista de Sprites
        self.player_list = None

        # Preparar al jugador
        self.rooms = None
        self.player_sprite = None
        self.physics_engine = None

        # Puntaje
        self.score = 0


        # Llevar seguimiento de las teclas persionadas
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False


    def setup(self):
        """ Preparar el juego e inicializar las variables"""

        # Lista de Sprite
        self.player_list = arcade.SpriteList()


        # Preparar al jugador
        self.player_sprite = arcade.Sprite(f"{ROUTE_SPRITES}/{PLAYER_SPRITE_NAME}", SPRITE_SCALING)
        self.player_sprite.center_x = PLAYER_INITIAL_POS_X
        self.player_sprite.center_y = PLAYER_INITIAL_POS_Y
        self.player_list.append(self.player_sprite)


        # --- Lista de rooms ---
        self.rooms = []

        # Crear los rooms
        room = stp.setup_room_open_right_up()
        self.rooms.append(room)
        room = stp.setup_room_open_left_up()
        self.rooms.append(room)
        room = stp.setup_room_open_left_down()
        self.rooms.append(room)
        room = stp.setup_room_open_right_down()
        self.rooms.append(room)

        # Numero de room inicial
        self.current_room = 0

        # Elegir el motor de físicas a usar
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)  # arcade.PhysicsEngine

        # Setear los límites de la vista
        # Éstos parámetros indicar hacia donde hemos "scrolleado"
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """ Dibujar en pantalla"""

        # Éste comando debe pasar antes de comenzar a dibujar
        self.clear()

        # Dibuja la textura de fondo
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)

        # Dibuja las paredes del room
        self.rooms[self.current_room].wall_list.draw()

        # Dibuja los coins de cada room
        self.rooms[self.current_room].coin_list.draw()

        # Dibuja puntaje
        output = f"Puntaje: {self.score}"
        arcade.draw_text(output, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30, arcade.color.BLACK, 14)

        # Dibujar Sprites
        self.player_list.draw()


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


        # Actualizar todos los sprites
        self.physics_engine.update()

        # Colision monedas
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].coin_list)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Lógica para saber en qué room estamos y si necesitamos ir a otro room

        # --- DENTRO DEL ROOM 0 (ROOM INICIAL ABIERTO DERECHA Y ARRIBA) ---
        # Si esta en el ROOM 0 y se pasa a la derecha entra al ROOM 1
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        # Si esta en el ROOM 0 y se pasa arriba entra al ROOM 3
        if self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 0:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0

        # --- DENTRO DEL ROOM 1 ( ABIERTO IZQUIERDA Y ARRIBA )
        # Si esta en el ROOM 1 y se pasa a la izquierda entra al ROOM 0
        if self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH
        # Si esta en el ROOM 1 y se pasa arriba entra al ROOM 2
        if self.player_sprite.center_y > SCREEN_HEIGHT and self.current_room == 1:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0

        # --- DENTRO DEL ROOM 2 ( ABIERTO IZQUIERDA Y ABAJO )
        # Si esta en el ROOM 2 y pasa a la izquierda entra al ROOM 3
        if self.player_sprite.center_x < 0 and self.current_room == 2:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH
        # Si esta en el ROOM 2 y pasa abajo entra al ROOM 1
        if self.player_sprite.center_y < 0 and self.current_room == 2:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT

        # --- DENTRO DEL ROOM 3 ( ABIERTO ABAJO Y DERECHA )
        # Si está en el ROOM 3 y se pasa abajo entra al ROOM 0
        if self.player_sprite.center_y < 0 and self.current_room == 3:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = SCREEN_HEIGHT
        # Si esta en el ROOM 3 y se pasa a la derecha entra al ROOM 2
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 3:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0







def main():
    """ Metodo principal"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
