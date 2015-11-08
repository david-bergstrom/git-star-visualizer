import pygame
from threading import Lock
from particle_manager import ParticleManager


class Visualizer:
    def __init__(self):
        # Dimensions
        self.screen_width = 1366
        self.screen_height = 768

        pygame.init()
        pygame.display.set_caption('Git Boom Visualizer')

        # Screen size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.DOUBLEBUF)

        self.particle_manager = ParticleManager(750, self.screen_width, self.screen_height)

        # Fps
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.lock = Lock()
        self.boost_left = 0

        self.font = pygame.font.SysFont("Source Sans Pro", 24)

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

            ms_elapsed = self.clock.tick(self.fps)
            self.particle_manager.update(ms_elapsed, self.boost_left)

            label = self.font.render(str(self.clock.get_fps()), 1, (255, 255, 255))
            self.screen.fill((0, 0, 0))
            self.screen.blit(label, (10, 10))
            self.particle_manager.draw(self.screen)
            pygame.display.flip()
