"""
A simple game to start playing with more Python stuff
"""
import sys
import videogamemainclass as vg
import arcade
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

print(sys.executable)
print(sys.version)
# print(arcade.__file__)

"""
A note for the future. The frame rate does not scale properly wiht the
speed of bullets (and perhaps of other sprites)
"""
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Videogame lib for fun!"


def main():
    """ Main method """
    game = vg.MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 1/30)
    game.setup()
    # arcade.pause(1)

#    window = arcade.get_window()
#    window._nswindow.setReleasedWhenClosed_(True)
    arcade.run()


if __name__ == "__main__":
    main()
