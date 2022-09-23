#!/usr/bin/env python3

import arcade
from typing import Optional
import math

# --- Constantes ---

SCREEN_TITLE = "Plataformero con fisicas"


# --- Parametros del juego ---
BACKGROUND_COLOR = arcade.color.AMAZON

# Tamaño de los tiles de nuestras imagenes
SPRITE_IMAGE_SIZE = 128

# Escala de los sprites
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_TILES = 0.5

# Tamaño del sprite escalado
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Tamaño de la rejilla a mostrar en pantalla, en numero de tiles
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT


# --- Físicas. A mayores números, más aceleración ---

# Gravedad
GRAVITY = 1500
BULLET_GRAVITY = 0

# Damping - Cantidad de velocidad que se pierde por segundo
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

# Fricción entre objetos
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Masa (El default es 1)
PLAYER_MASS = 2.0
BULLET_MASS = 0.1

# Evita que el player vaya muy rápido
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600

# FUERZAS

# Fuerza para las balas
BULLET_MOVE_FORCE = 6000


# Fuerza que se aplica para el movimiento lateral en el suelo
PLAYER_MOVE_FORCE_ON_GROUND = 8000

# Fuerza al movimiento lateral en el aire
PLAYER_MOVE_FORCE_ON_AIR = 1500

# Fuerza del salto
PLAYER_JUMP_IMPMULSE = 1800
PLAYER_JUMP_WALL_IMPULSE = 1300

# Fuerza del dash
DASH_MOVE_IMPULSE = 900

# --- Animaciones ----
# Zona muerta para entrar a animación de Idle
DEAD_ZONE = 0.1

# Constantes para ver si se está mirando a la derecha o izquierda
RIGHT_FACING = 0
LEFT_FACING = 1

# Cuantos pixeles moverse antes de cambiar a la animación de caminar
DISTANCES_TO_CHANGE_TEXTURE = 20

# --- Control de Cámara ---

# Márgen de cuántos pixel mínimo mantener entre el personaje y el borde de la pantalla
VIEWPOINT_MARGIN = 200

# Velocidad en que la cámara persigue al jugador, 1 es instantáneo
CAMERA_SPEED = 0.1

class PlayerSprite(arcade.Sprite):
    """ Player Sprite"""
    def __init__(self):
        super().__init__()

        # Escala de sprite
        self.scale = SPRITE_SCALING_PLAYER

        main_path = ":resources:images/animated_characters/female_person/femalePerson"

        # Cargar texturas
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")

        # Cargar animación de caminar
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Textura inicial
        self.texture = self.idle_texture_pair[0]

        # el Hit Box se va a setear usando la primera imagen cargada
        self.hit_box = self.texture.hit_box_points

        # Mirar a la derecha por defecto
        self.character_face_direction = RIGHT_FACING

        # Index de la textura actual
        self.cur_texture = 0

        # Que tan lejos tenemos que caminar horizontalmente para cambiar la textura
        self.x_odometer = 0

    def pymunk_moved(self, physics_egine, dx, dy, d_angle):
        """ Se encarga del movimiento hecho por el motor pymunk"""

        # Ver si debemos mirar a la derecha o izquierda
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Variable para checkear si estamos pisando algo
        is_on_ground = physics_egine.is_on_ground(self)

        # Añade al odometro cuan lejos nos hemos movido
        self.x_odometer += dx

        # Animación de salto
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        # Amimación Idle
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Confirmar si nos hemos movido lo suficiente como para cambiar la textura
        if abs(self.x_odometer) > DISTANCES_TO_CHANGE_TEXTURE:

            # Resetea el odometro
            self.x_odometer = 0

            # Crea un "loop" cambiando entre las texturas 0 a la 7, pasando por las 8 texturas totales
            # Si tenemos una animacion de caminar de menos frames, ajustar los numeros para que haga
            # loop por cada frame
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class MyGame(arcade.Window):
    """ Clase Window custom"""
    def __init__(self):
        """ Inicializador """
        # Llama a la clase init del padre
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Lista de Sprites
        self.player_list : Optional[arcade.SpriteList] = None
        self.wall_list : Optional[arcade.SpriteList] = None
        self.bullet_list : Optional[arcade.SpriteList] = None
        self.item_list : Optional[arcade.SpriteList] = None

        # Preparar al jugador
        self.player_sprite : Optional[PlayerSprite] = None
        self.physics_engine : None

        # Variable para manejar el puntaje
        self.score : int = 0

        # Contador de saltos
        self.jump_count: int = 0
        self.dash_count: int = 0

        # Physics Engine
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        # Se usan para manejar el scroll de camara
        self.view_bottom = 0
        self.view_left = 0

        # Llevar seguimiento de las teclas persionadas
        self.left_pressed : bool = False
        self.right_pressed : bool = False
        self.up_pressed : bool = False
        self.down_pressed : bool = False


    def setup(self):
        """ Preparar el juego e inicializar las variables"""

        # Color de fondo
        arcade.set_background_color(BACKGROUND_COLOR)

        # Lista de Sprite
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Nombre del mapa
        map_name = ":resources:/tiled_maps/pymunk_test_map.json"

        # Cargar el mapa de tile
        tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)

        # Sacar los sprites desde las capas del mapa
        self.wall_list = tile_map.sprite_lists["Platforms"]
        self.item_list = tile_map.sprite_lists["Dynamic Items"]

        # Preparar al jugador
        self.player_sprite = PlayerSprite()

        # Posición del jugador
        grid_x = 1
        grid_y = 1
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        # Añade el sprite a la lista
        self.player_list.append(self.player_sprite)


        # --- Preparación de sistema de físicas Pymunk ---
        # El damping por defecto de cada objeto controla el porcentaje de velocidad
        # que el objeto mantiene cada segundo. Un valor de 1.0 represanta ninguna
        # pérdida de velocidad, 0.9 pierde 10% de velocidad por segundo.
        # Para juegos con vista desde arriba, ésta es basicamente la fricción para
        # los objetos que se pueden interactuar y mover.
        # Para plataformeros con gravedad, lo mejor es setear damping a 1.0
        # El default es 1.0 si no se especifica
        damping = DEFAULT_DAMPING

        # Setear la gravedad. (0, 0) es bueno para juegos del espacio exterior y
        # vista desde arriba
        gravity = (0, -GRAVITY)

        # Crear el physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=gravity)

        # Añade el jugador
        # Para el jugador, seteamos el damping a un valor más bajo lo que incrementa
        # el ratio de damping. Ésto prevee que el personaje se desplaze muy lejos
        # una vez el jugador deja de presionar las telcas de movimiento.
        # Asignar el moment a PymunkPhysicsEngine.MOMENT_INF previene las rotaciones.
        # La fricción normalmente va entre 0 (Sin fricción) y 1.0 (Mucha Fricción)
        # fricción se produce entre dos objetos que entran en contacto. Es importante
        # recordar que en los juegos de vista desde arriba donde la fricción que se
        # mueve junto al "suelo" se controla con el damping
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        # Crear las murallas
        # Al asignar el body type a PymunkPhysicsEngine.STATIC las murallas no se
        # pueden mover
        # Los objetos movibles que responden a fuerzas se les asigna el body type
        # PymunkPhysicsEngine.DYNAMIC
        # El body type PymunkPhysicsEngine.KINEMATIC hará que los objetos se muevan
        # pero se asume que el movimiento será hecho por código y no responden
        # a fuerzas físicas.
        # El body type DYNAMIC es el valor por defecto
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        # Añadir los items
        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="item")

        # Setear los límites de la vista
        # Éstos parámetros indicar hacia donde hemos "scrolleado"
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """ Dibujar en pantalla"""

        # Éste comando debe pasar antes de comenzar a dibujar
        self.clear()

        # Seleccionar cámara donde dibujar los sprites
        # self.camera_sprites.use()

        # Dibujar Sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.bullet_list.draw()
        self.item_list.draw()

        # Dibujar el puntaje
        output = f"Puntaje: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        # Seleccionar la cámara inmóvil para GUI
        # self.camera_gui.use()

        # Dibujar la GUI
        # ... TODO


    def on_key_press(self, key, modifiers):
        """ Se llama cada vez que se presiona una tecla"""

        if key == arcade.key.W:
            self.up_pressed = True
            # Ver si el jugador está en el suelo
            if self.physics_engine.is_on_ground(self.player_sprite) and self.jump_count < 1:
                # Está en el suelo, entonces salta
                impulse = (0, PLAYER_JUMP_IMPMULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
            elif arcade.check_for_collision_with_list(self.player_sprite, self.wall_list) and self.jump_count <1:
                impulse = (0, PLAYER_JUMP_WALL_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
                self.jump_count += 1
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.ESCAPE:
            arcade.exit()
        elif key == arcade.key.R:
            self.setup()

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

    def on_mouse_press(self, x, y, button, modifiers):
        """ Se llama cada vez que se hace un click"""


        def dash(self):
            """ La idea es hacer que el personaje haga un "dash" hacia
            la dirección del puntero del mouse, aqui hay prototipos
            y pruebas"""

            vel_x = 0
            vel_y = 0

            rel_x = x - self.player_sprite.center_x
            rel_y = y - self.player_sprite.center_y
            print(rel_x , rel_y)
            if -20 < rel_x < 15 and rel_y < 0 and self.dash_count < 1:
                vel_x = 0
                vel_y = -DASH_MOVE_IMPULSE
                self.dash_count += 1
            elif -20 < rel_x < 15 and rel_y > 0 and self.dash_count < 1:
                vel_x = 0
                vel_y = DASH_MOVE_IMPULSE
                self.dash_count += 1
            elif -30 < rel_y < 15 and rel_x > 0 and self.dash_count < 1:
                vel_x = DASH_MOVE_IMPULSE
                vel_y = 0
                self.dash_count += 1
            elif -30 < rel_y < 15 and rel_x < 0 and self.dash_count < 1:
                vel_x = -DASH_MOVE_IMPULSE
                vel_y = 0
                self.dash_count += 1
            elif rel_y < -30 and rel_x > 15 and self.dash_count < 1:
                vel_x = DASH_MOVE_IMPULSE
                vel_y = -DASH_MOVE_IMPULSE
                self.dash_count += 1
            elif rel_y > 15 and rel_x < -20 and self.dash_count < 1:
                vel_x = -DASH_MOVE_IMPULSE
                vel_y = DASH_MOVE_IMPULSE
                self.dash_count += 1
            elif rel_y < -30 and rel_x < -20 and self.dash_count < 1:
                vel_x = -DASH_MOVE_IMPULSE
                vel_y = -DASH_MOVE_IMPULSE
                self.dash_count += 1
            elif rel_y > 15 and rel_x > 15 and self.dash_count < 1:
                vel_x = DASH_MOVE_IMPULSE
                vel_y = DASH_MOVE_IMPULSE
                self.dash_count += 1


            self.physics_engine.set_velocity(self.player_sprite, (vel_x, vel_y))

        def spawn_bullet(self):
            bullet = arcade.SpriteSolidColor(20, 5, arcade.color.DARK_YELLOW)
            self.bullet_list.append(bullet)

            # Deja la bala en la locación actual del jugador
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.position = self.player_sprite.position

            # Obtener desde el mouse el destino de la bala
            # IMPORTANTE!! Si se tiene una pantalla con Scroll,
            # tambien se debe sumar self.view_bottom y self.view_left
            dest_x = x
            dest_y = y

            # Calcular el destino de la bala
            # Se calcula en angulo en radianes entre las posiciones iniciales
            # y finales. Ésto da como resultado el ángulo en el que la bala
            # va a viajar
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Calcular el 1/2 del sprite, para saber qué tan lejos dibujar la bala
            size = max(self.player_sprite.width, self.player_sprite.height) / 2

            # Usar ángulos para spawnear balas con el angulo correcto
            bullet.center_x += size * math.cos(angle)
            bullet.center_y += size * math.sin(angle)

            # Definir el angulo de la bala
            bullet.angle = math.degrees(angle)

            # Gravedad que afecta a la bala
            bullet_gravity = (0, -BULLET_GRAVITY)

            # Añade el sprite. Esto se DEBE hacer DESPUES de definir los campos anteriores
            self.physics_engine.add_sprite(bullet,
                                           mass=BULLET_MASS,
                                           damping=1.0,
                                           friction=0.6,
                                           collision_type="bullet",
                                           gravity=bullet_gravity,
                                           elasticity=0.9)

            # Añade fuerza a la bala
            force = (BULLET_MOVE_FORCE, 0)
            self.physics_engine.apply_force(bullet, force)


        if button == arcade.MOUSE_BUTTON_LEFT:
            spawn_bullet(self)
        elif button == arcade.MOUSE_BUTTON_RIGHT and self.dash_count < 1:
            dash(self)

    def on_update(self, delta_time):
        """ Movimiento y lógica del juego"""

        # Actualizar la fuerza aplicada al movimiento del jugador
        # dependiendo de las teclas presionadas

        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        if is_on_ground:
            self.jump_count = 0
            self.dash_count = 0

        # Resetar la cuenta de saltos si toca el suelo

        if self.left_pressed and not self.right_pressed:
            # Crea una fuerza a la izquierda y la aplica
            if is_on_ground:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-PLAYER_MOVE_FORCE_ON_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Asignar una fricción de 0 al jugador mientras se mueve
            # para que no afecte el movimiento al correr
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Crea una fuerza a la derecha y la aplica
            if is_on_ground:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (PLAYER_MOVE_FORCE_ON_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Asignar una fricción de 0 al jugador mientras se mueve
            # para que no afecte el movimiento al correr
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            # Mientras el jugador no se mueve subir la fricción
            # para detenerse
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        # Ver si el player choca con una moneda
        # coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        # Revisar lista de hits y eliminar de la lista cada moneda chocada, y sumar 1 al puntaje
        # for coin in coins_hit_list:
            # coin.remove_from_sprite_lists()
            # self.score += 1

        # Actualizar todos los sprites
        self.physics_engine.step()

        # Mover la pantalla al jugador
        # self.scroll_to_player()

    # def scroll_to_player(self):
    #     """
    #     Mueve la pantalla al jugador
    #     Éste método intentará mantener al jugador al menos a
    #     VIEWPORT_MARGIN pixel de distancia del borde

    #     Si CAMERA_SPEED es 1, la cámara se moverá inmediatamente
    #     a la poscisión deseada. Cualquier valor entre 0 y 1
    #     hará que la cámara se mueva de manera más fluida
    #     """

    #     # --- Controlar el Scroll ---

    #     # Hacia la izquierda
    #     left_boundary = self.view_left + VIEWPOINT_MARGIN
    #     if self.player_sprite.left < left_boundary:
    #         self.view_left -= left_boundary - self.player_sprite.left

    #     # Hacia la derecha
    #     right_boundary = self.view_left + self.width - VIEWPOINT_MARGIN
    #     if self.player_sprite.right > right_boundary:
    #         self.view_left += self.player_sprite.right - right_boundary

    #     # Hacia Arriba
    #     top_boundary = self.view_bottom + self.height - VIEWPOINT_MARGIN
    #     if self.player_sprite.top > top_boundary:
    #         self.view_bottom += self.player_sprite.top - self.player_sprite.bottom

    #     # Hacia Abajo
    #     bottom_boundary = self.view_bottom + VIEWPOINT_MARGIN
    #     if self.player_sprite.bottom < bottom_boundary:
    #         self.view_bottom -= bottom_boundary - self.player_sprite.bottom

    #     # Scrollear a la ubicación correcta
    #     position = self.view_left, self.view_bottom
    #     self.camera_sprites.move_to(position, CAMERA_SPEED)


    def on_resize(self, width, height):
        # self.camera_sprites.resize(int(width), int(height))
        # self.camera_gui.resize(int(width), int(height))
        pass




def main():
    """ Metodo principal"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
