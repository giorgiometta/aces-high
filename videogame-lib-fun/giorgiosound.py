"""
Some simple stuff to deal with sound
"""

import pyglet.media as pg


class ContinuousSound():
    """ Giorgio simple class for Continuous Sound, straight in Pyglet """

    def on_eos(self):
        pass

    def __init__(self, filename):
        # Set up sound
        self.player = pg.Player()
        self.player.loop = True
        self.source = pg.StaticSource(pg.load(filename))
        self.player.queue(self.source)
        # self.player.push_handlers(self.on_eos)

    def play(self):
        self.player.play()


class OneShotSound():
    """ Simple sound, play it once and auto reset """

    def __init__(self, filename):
        self.player = pg.Player()
        self.player.loop = False
        self.source = pg.StaticSource(pg.load(filename))
        # self.player.queue(self.source)

    def play(self):
        self.player.queue(self.source)
        self.player.play()
