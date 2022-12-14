import pygame as pg
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.1)
        laser_sound = pg.mixer.Sound('sounds/laser.wav')
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')
        big_alien_sound = pg.mixer.Sound('sounds/big_alien_moves.wav')
        self.sounds = {'laser': laser_sound, 'gameover': gameover_sound, 'alien': big_alien_sound}

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def shoot_laser(self): pg.mixer.Sound.play(self.sounds['laser'])
    def big_alien_move(self): pg.mixer.Sound.play(self.sounds['alien'])
    def big_alien_stop(self): pg.mixer.Sound.stop(self.sounds['alien'])
    def gameover(self):
        self.stop_bg()
        self.big_alien_stop()
        pg.mixer.music.load('sounds/gameover.wav')
        self.play_bg()
        time.sleep(2.8)
        self.stop_bg()

    def speedup(self):
        self.stop_bg()
        pg.mixer.music.load('sounds/startrek_speed.wav')
        self.play_bg()

    def speedup2(self):
        self.stop_bg()
        pg.mixer.music.load('sounds/startrek_speed_two.wav')
        self.play_bg()
