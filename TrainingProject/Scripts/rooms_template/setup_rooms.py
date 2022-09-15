#!/usr/bin/env python3

import arcade

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

class Room:
    """
    Ésta clase contiene toda la información acerca de las diferentes "habitaciones"
    """

    def __init__(self):
        # Aqui se deben agregar las listas para los elementos del cuarto.
        # Monedas, Mounstruos, obstáculos, etc.
        self.wall_list = None

        self.coin_list = None

        # Ésta variable contiene la imagen de fondo.
        # Si no quieres un fondo diferente, ésta parte se puede omitir

def setup_room_open_right():
    """
    Crea y devuelve el cuarto con una apertura a la derecha
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or x == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 7 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Cargar monedas ---
    coin = arcade.Sprite(f"{ROUTE_SPRITES}/{COIN_SPRITE_NAME}", SPRITE_SCALING)
    coin.center_x = 200
    coin.center_y = 200
    room.coin_list.append(coin)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

    return room

def setup_room_open_left():
    """
    Crea y devuelve el cuarto con una apertura a la izquierda
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or x != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_open_up():
    """
    Crea y devuelve el cuarto con una apertura arriba
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or y == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room


def setup_room_open_down():
    """
    Crea y devuelve el cuarto n°3
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or y != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_open_left_right():
    """
    Crea y devuelve el cuarto con aperturas a la izquierda y derecha
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if ( y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or ( x != 0 and x == 0 ):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room
def setup_room_open_up_down():
    """
    Crea y devuelve el cuarto con aperturas arriba y abajo
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or ( y != 0 and y == 0 ):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
              wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
              wall.left = x
              wall.bottom = y
              room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_open_left_up():
    """
    Crea y devuelve el cuarto con aperturas a la izquierda y arriba
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or y == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

     # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or x != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_open_left_down():
    """
    Crea y devuelve el cuarto con aperturas a la izquierda y abajo
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or y != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

     # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or x != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_open_right_up():
    """
    Crea y devuelve el cuarto con aperturas a la derecha y arriba
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or y == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

     # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or x == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_open_right_down():
    """
    Crea y devuelve el cuarto con aperturas a la derecha y abajo
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or y != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

     # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or x == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_open_all():
    """
    Crea y devuelve el cuarto con aperturas en todas las direcciones
    Si el programa se vuelve muy grande, es mejor separar éstos setup en diferentes archivos
    """
    room = Room()

    # --- Prepara e inicializa las variables ---
    # Listas de sprites
    room.wall_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # --- Prepara las paredes ---
    # Crea paredes en la parte superior e inferior

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):  # Ésta "y" loopea una lista de dos, la coordenada 0 y justo debajo de la parte superior de la pantalla
        # Un loop para crear las paredes entre el punto anterior
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if ( x != SPRITE_SIZE * 6 and x != SPRITE_SIZE * 7 ) or (y != 0 and y ==0):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

     # Crea paredes en los laterales
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 ) or (x == 0 and x != 0):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)

    # --- Imagen de fondo ---
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room
