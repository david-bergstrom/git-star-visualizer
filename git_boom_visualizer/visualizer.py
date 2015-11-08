import pygame
from threading import Lock
from particle_manager import ParticleManager


class Visualizer:
    def __init__(self):
        # Dimensions
        self.screen_width = 640
        self.screen_height = 480

        pygame.init()
        pygame.display.set_caption('Git Boom Visualizer')

        # Screen size
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))

        texture = pygame.image.load('git_boom_visualizer/circle.png')
        self.particle_manager = ParticleManager(200, texture, self.screen_width, self.screen_height)

        # Fps
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.lock = Lock()
        self.boost_left = 0

    def post(self):
        with self.lock:
            self.boost_left = 1000

    def run(self):
        while True:
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break

            if self.lock.acquire(False):
                if self.boost_left > 0:
                    self.boost_left -= 1
                    print self.boost_left

                self.lock.release()

            pygame.display.update()
            ms_elapsed = self.clock.tick(self.fps)
            self.particle_manager.update(ms_elapsed, self.boost_left)

            self.screen.fill((0, 0, 0))
            self.particle_manager.draw(self.screen)
