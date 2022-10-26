"""
I'm putting here the main class of the game.
"""
# import pyglet
import arcade
import additionalsprites as adsp
import giorgiosound as gs


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title, rate=1/30):
        super().__init__(width, height, title, update_rate=rate)

        # Main game-wide parameters
        print('Game running at:', round(rate, 2), 'seconds')
        self._FLYING_SPEED = int(60*rate)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.player_list = None
        self.player_sprite = None
        self.background_list = None
        self.ground_enemy_list = None
        self.flying_enemy_list = None
        self.bullet_list = None
        self.bomb_list = None
        self.pre_loaded_textures = []

        # Sound
        self.background_music = None
        self.shot_sound = None
        self.bullet_sound = None
        self.explosion_sound = None

        # score and other game specific globals
        self._score = 1234567

    def on_eos(self):
        print('eos')

    def setup(self):
        # Set defaults/create objects here
        # arcade.set_background_color(arcade.color.AMAZON)

        # Pre-load textures for faster sprite creation
        self.pre_loaded_textures = []
        for i in range(1, 5):
            texture_name = f"images/WaterBomb{i:d}.png"
            self.pre_loaded_textures.append(arcade.load_texture(texture_name))
        for i in range(1, 6):
            texture_name = f"images/WaterExplosion{i:d}.png"
            self.pre_loaded_textures.append(arcade.load_texture(texture_name))
        for i in range(4, 0, -1):
            texture_name = f"images/WaterExplosion{i:d}.png"
            self.pre_loaded_textures.append(arcade.load_texture(texture_name))
        # Load 14 frames of explosion
        for i in range(0, 55, 4):
            texture_name = f"images/explosion{i:04d}.png"
            self.pre_loaded_textures.append(arcade.load_texture(texture_name))
        texture_name = "images/Shot2.png"
        self.pre_loaded_textures.append(arcade.load_texture(texture_name))
        # Load 14 frames of explosion
        for i in range(0, 55, 4):
            texture_name = f"images/explosion{i:04d}.png"
            self.pre_loaded_textures.append(arcade.load_texture(texture_name))

        # Keep adding textures here, whatever name they have

        # Create the sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        viewport = arcade.get_viewport()
        self.player_sprite = adsp.MainCharacter(self._FLYING_SPEED,
                                                viewport[1]-viewport[0])
        self.player_sprite.set_character_position(
            (viewport[0]+viewport[1])/2,
            (viewport[2]+viewport[3])/4)
        self.player_list.append(self.player_sprite)

        # Create the background list - everything we don't interact with
        self.background_list = arcade.SpriteList()
        background = arcade.Sprite("images/Background.png")
        background.bottom = 0
        background.left = 0
        self.background_list.append(background)

        # Create the enemy list - obvious meaning
        self.ground_enemy_list = arcade.SpriteList()
        self.flying_enemy_list = arcade.SpriteList()

        # --- Load in the enemy sprites from the tiled editor ---
        my_map = arcade.read_tiled_map("./Scenarios.tmx", 1.0)
        tile_list = arcade.generate_sprites(my_map, 'Ground Enemies', 1.0)
        for i in tile_list:
            self.ground_enemy_list.append(i)
        tile_list = arcade.generate_sprites(my_map, 'Flying Enemies', 1.0)
        for i in tile_list:
            self.flying_enemy_list.append(i)

        # Bullet list, all bullets go here
        self.bullet_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()

        # Just for testing purposes
        # self.test = adsp.WaterBomb(100, 900, 50, 1,
        #                            self.pre_loaded_textures[0:9])
        # self.background_list.append(self.test)

        # --- Other stuff
        # Set the background color
        # if my_map.backgroundcolor:
        #    arcade.set_background_color(my_map.backgroundcolor)

        # Set up sound
        self.background_music = gs.ContinuousSound('sounds/bground.wav')
        self.background_music.play()
        self.background_music.player.volume = 0.1
        self.shot_sound = gs.OneShotSound('sounds/shot.wav')
        self.shot_sound.player.volume = 1.0
        self.bullet_sound = gs.OneShotSound('sounds/shot2.wav')
        self.bullet_sound.player.volume = 1.0
        self.explosion_sound = gs.OneShotSound('sounds/explosion.wav')
        self.explosion_sound.player.volume = 1.0

        # arcade.sound.play_sound(self.background_music)
        # print(self.background_music.player)
        # self.background_music.player.push_handlers(on_eos)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last
        # frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.background_list.draw()
        self.ground_enemy_list.draw()
        self.bomb_list.draw()
        self.bullet_list.draw()
        self.flying_enemy_list.draw()
        self.player_list.draw()

        viewport = arcade.get_viewport()
        score_text = f'SCORE: {self._score:7}'
        arcade.draw_text(score_text, viewport[1] - 170, viewport[2] + 10,
                         arcade.csscolor.BLACK, 18)
        score_text = f'HI SCORE: {self._score:7}'
        arcade.draw_text(score_text, viewport[0]+10, viewport[2] + 10,
                         arcade.csscolor.BLACK, 18)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()
        self.player_list.update_animation()
        self.background_list.update()
        self.background_list.update_animation()
        self.bullet_list.update()
        self.bullet_list.update_animation()
        self.bomb_list.update()
        self.bomb_list.update_animation()

        # The flying logic
        # TO BE COMPLETED
        _viewport = arcade.get_viewport()
        arcade.set_viewport(_viewport[0], _viewport[1],
                            _viewport[2]+self._FLYING_SPEED,
                            _viewport[3]+self._FLYING_SPEED)

        # Collisions
        for enemy in self.ground_enemy_list:
            hit_list = arcade.check_for_collision_with_list(enemy,
                                                            self.bomb_list)
            if len(hit_list) > 0:
                for bullet in hit_list:
                    if isinstance(bullet, adsp.WaterBomb) and\
                            bullet.cur_texture_index == 4:
                        bullet.center_x = enemy.center_x
                        bullet.center_y = enemy.center_y
                        bullet.cur_texture_index = 13
                        enemy.kill()
                        self.explosion_sound.play()

        for enemy in self.flying_enemy_list:
            hit_list = arcade.check_for_collision_with_list(enemy,
                                                            self.bullet_list)
            if len(hit_list) > 0:
                for bullet in hit_list:
                    if isinstance(bullet, adsp.SimpleBullet):
                        bullet.center_x = enemy.center_x
                        bullet.center_y = enemy.center_y
                        bullet.cur_texture_index = 1
                        enemy.kill()
                        self.explosion_sound.play()

        # check time elapsed since last call
        # print(delta_time)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """

        if key == arcade.key.LEFT:
            self.player_sprite.turn_character_counterclockwise()
        elif key == arcade.key.RIGHT:
            self.player_sprite.turn_character_clockwise()
        elif key == arcade.key.SPACE or key == arcade.key.S:
            self.player_sprite.fire_bomb(self.pre_loaded_textures[0:27],
                                         self.bomb_list,
                                         self.shot_sound)
        elif key == arcade.key.A:
            self.player_sprite.fire_bullet(self.pre_loaded_textures[27:41],
                                           self.bullet_list,
                                           self.bullet_sound)
        elif key == arcade.key.Q:
            self.close()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass
