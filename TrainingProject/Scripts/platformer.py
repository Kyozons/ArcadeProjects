#!/usr/bin/env python3

import arcade

# --- CONSTANTES ---
SCREEN_WIDTH = 1000
SCREEN_HEIGTH = 650
TITLE = "Plataformero"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5

GRAVITY = 5
PLAYER_MOVE_SPEED = 7
PLAYER_JUMP_SPEED = 90
class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGTH, TITLE)


        self.scene = None

        self.player_sprite = None

        self.score = 0

        self.physics_engine = None

        # Llevar seguimiento de las teclas persionadas
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False


        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins")


        self.score = 0

        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)


        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)


        coordinate_list = [[256, 96], [512, 96], [512, 160], [512, 224] , [768, 96], [832, 96], [832, 160], [892, 96], [892, 160], [892, 224]]

        for coordinate in coordinate_list:
            coin = arcade.Sprite("../Assets/Sprites/coin_01.png", TILE_SCALING / 2)
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
            coin.center_x = coordinate[0]
            coin.center_y = coordinate[1] + 64
            self.scene.add_sprite("Coins", coin)
            check_coins_in_box = arcade.check_for_collision_with_list(wall, self.scene.get_sprite_list("Coins"))
            for coin in check_coins_in_box:
                coin.remove_from_sprite_lists()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"])

    def on_draw(self):
        self.clear()

        self.scene.draw()

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
        if key == arcade.key.R:
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


    def on_update(self, delta_time):
        # Calcular la velocidad en base a las teclas presionadas
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVE_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVE_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVE_SPEED

        self.physics_engine.update()

        check_coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("Coins"))
        for coin in check_coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
