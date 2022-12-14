class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 191, 255)
        self.GREEN = (0, 255, 0)
        self.bg_color = (0, 0, 0)

        self.laser_width = 5
        self.laser_height = 30
        self.laser_color = 255, 0, 0
        self.lasers_every = 10

        self.alien_points = 50
        self.ship_limit = 3

        self.fleet_drop_speed = 3
        self.fleet_direction = 1
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.alien_speed_factor = 0.5
        self.big_alien_speed_factor = 2
        self.ship_speed_factor = 5
        self.laser_speed_factor = 6

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale
