"""
A variety of specialized sprites to create nice functionalities.
"""
import arcade
import numpy as np


class BombInWater(arcade.AnimatedTimeSprite):
    """
    A container to manage a bomb in water (let's see if I manage to do it)
    """

    def __init__(self, scale):
        super().__init__(scale)
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion1.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion2.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion3.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion4.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion5.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion4.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion3.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion2.png", scale=scale))
        self.textures.append(arcade.load_texture(
            "images/WaterExplosion1.png", scale=scale))


class EnemyBullet(arcade.Sprite):
    """
    The enemy bullets, not animated, simple...
    For the time being, I'll keep track of the number of instances...
    just to check things don't spiral out of control
    """
    number_of_bullets = 0

    def __init__(self, x, y, speed, direction, texture):
        super().__init__(scale=1.0)
        self.texture = texture
        self.center_x = x
        self.center_y = y
        self.change_x = speed * np.cos(direction*np.pi/180)
        self.change_y = speed * np.sin(direction*np.pi/180)
        EnemyBullet.number_of_bullets += 1

    def update(self):
        super().update()
        viewport = arcade.get_viewport()
        if self.right < viewport[0] or\
                self.left > viewport[1] or\
                self.bottom > viewport[3] or\
                self.top < viewport[2]:
            self.kill()
            EnemyBullet.number_of_bullets -= 1


class SimpleBullet(arcade.AnimatedTimeSprite):
    """
    A simple bullet of the main character
    It uses the pre-loaded texture number 68
    and the standard explosion textures
    """
    number_of_bullets = 8

    def __init__(self, x, y, angle, interval, speed, textures):
        super().__init__(scale=0.3)
        self.textures = textures
        self.current_texture = 0
        self.texture_change_frames = interval
        self.center_x = x
        self.center_y = y
        self.angle = angle
        self.change_x = speed * np.cos((angle+90)*np.pi/180)
        self.change_y = speed * np.sin((angle+90)*np.pi/180)
        self.set_texture(self.current_texture)

    def update_animation(self):
        """
        Logic for selecting the proper texture to use.
        when cur_texture_index == 0 do nothing
        == 1 starts explosion
        > 1 animate explosion and then self destruct
        """
        if (self.cur_texture_index == 1):
            ''' explode '''
            self.change_x = 0
            self.change_y = 0
            self.cur_texture_index = 2
        elif (self.cur_texture_index > 1):
            if self.frame % self.texture_change_frames == 0:
                self.cur_texture_index += 1

            if self.cur_texture_index >= len(self.textures):
                self.kill()
                SimpleBullet.number_of_bullets += 1
                return

            self.set_texture(self.cur_texture_index)
            self.frame += 1

    def update(self):
        super().update()
        viewport = arcade.get_viewport()
        if self.right < viewport[0] or\
           self.left > viewport[1] or\
           self.bottom > viewport[3]:
            self.kill()
            SimpleBullet.number_of_bullets += 1


class WaterBomb(arcade.AnimatedTimeSprite):
    """
    A container to manage the bomb itself
    textures are loaded in the following pattern:
    0-3: flying bomb opening (4)
    4-8: water explosion (5)
    9-12: water explosion (4)
    13-26: explosion (54)
    """
    number_of_bombs = 5

    def __init__(self, x, y, interval, speed, textures):
        super().__init__(scale=1)
        self.textures = textures
        self.current_texture = 0
        self.texture_change_frames = interval
        self.center_x = x
        self.center_y = y
        self.change_y = speed
        # self.increment = 1
        self.set_texture(self.current_texture)

    def update_animation(self):
        """
        Logic for selecting the proper texture to use.
        """
        if self.frame % self.texture_change_frames == 0:
            self.cur_texture_index += 1
            if self.cur_texture_index == 4:
                self.change_y = 0
                self.texture_change_frames /= 5
            elif self.cur_texture_index == 13:
                self.kill()
                WaterBomb.number_of_bombs += 1
                return
            elif self.cur_texture_index == 14:
                self.change_y = 0
                self.texture_change_frames = 1
                # self.increment = 3

            if self.cur_texture_index >= len(self.textures):
                self.kill()
                WaterBomb.number_of_bombs += 1
                return

            self.set_texture(self.cur_texture_index)
        self.frame += 1


class Explosion(arcade.AnimatedTimeSprite):
    """
    An explosion
    """

    def __init__():
        pass


class MainCharacter(arcade.AnimatedTimeSprite):
    """
    A container to manage the main character of the game
    """

    def __init__(self, flying_speed, win_width):
        self._scale = 1.0
        self._player_rotation_speed = 5 * flying_speed
        self._player_translation_speed = 3 * flying_speed / 2
        super().__init__(scale=self._scale)
        self.textures.append(arcade.load_texture(
            "images/Plane1.png", scale=self._scale))
        self.textures.append(arcade.load_texture(
            "images/Plane2.png", scale=self._scale))
        self.textures.append(arcade.load_texture(
            "images/Plane3.png", scale=self._scale))
        self._flying_speed = flying_speed
        self._win_width = win_width

    def set_character_position(self, x, y):
        """ Set the center position of the main character """
        self.center_x = x
        self.center_y = y

    def turn_character_clockwise(self):
        """ Rotate clockwise """
        self.change_angle = -self._player_rotation_speed

    def turn_character_counterclockwise(self):
        """ Rotate counterclockwise """
        self.change_angle = self._player_rotation_speed

    def stop_turning(self):
        """ Stop rotation """
        self.change_angle = 0

    def update(self):
        """ My logic for update """
        self.center_y += self._flying_speed
        if self.angle < -0.5:
            self.center_x += self._player_translation_speed
        elif self.angle > 0.5:
            self.center_x -= self._player_translation_speed

        super().update()

        _min = (self.center_x-self._win_width+self.width/2)\
            * 90/(self._win_width-self.width/2)
        _max = (self.center_x-self.width/2)\
            * 90/(self._win_width-self.width/2)
        if self.angle < _min:
            self.angle = _min
        elif self.angle > _max:
            self.angle = _max

    def fire_bomb(self, textures, sprite_list, sound):
        """ Fire a bomb """
        if WaterBomb.number_of_bombs > 0:
            bomb = WaterBomb(self.center_x, self.top+textures[0].height,
                             int(30/self._flying_speed+.5),
                             self._flying_speed*3, textures)
            sprite_list.append(bomb)
            sound.play()
            WaterBomb.number_of_bombs -= 1

    def fire_bullet(self, textures, sprite_list, sound):
        """ Fire a bullet """
        if SimpleBullet.number_of_bullets > 0:
            bullet = SimpleBullet(self.center_x, self.center_y,
                                  self.angle, int(1/self._flying_speed+.5),
                                  self._flying_speed*7, textures)
            sprite_list.append(bullet)
            sound.play()
            SimpleBullet.number_of_bullets -= 1
