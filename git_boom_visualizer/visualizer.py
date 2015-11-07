import pygame

from threading import Lock
from random import Random
from math import cos, sin, pi

class Particle:
    def __init__(self, x, y, angle, angular_velocity, ttl, size):
        self.x = x
        self.y = y
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.ttl = ttl
        self.size = size
    
    def update(self, time):
        self.ttl -= 1
        self.x += self.angular_velocity * cos(self.angle)
        self.y += self.angular_velocity * sin(self.angle)
        
        return self.ttl > 0

    def get_pos(self):
        return (int(self.x), int(self.y))

    def shift_center(self, pos, image):
        shift = (- image.get_width() / 2.0, - image.get_height() / 2.0)
        return map(sum, zip(pos, shift))

    def draw(self, screen, texture):
        pos = self.get_pos()
        screen.blit(texture, self.shift_center(pos, texture))

class ParticleManager():
    def __init__(self, particle_count, texture):
        self.particle_count = particle_count
        self.texture = texture

        self.rand = Random()
        self.particles = []
        for i in range(particle_count):
            self.particles.append(self.random_particle())

    def update(self, ms_elapsed, boost):
        self.particles = filter(lambda particle :
                                particle.update(ms_elapsed),
                                self.particles)
        
        for i in range(self.particle_count - len(self.particles) + boost):
            self.particles.append(self.random_particle(boost))

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen, self.texture)

    def random_particle(self, boost=0):
        randint = self.rand.randint
        return Particle(randint(100, 500), randint(470, 480),
                        self.rand.uniform(-0.3, 0.3) - pi / 2,
                        randint(1, 5), randint(5, 60), 100)
                        

class Visualizer:
    def __init__(self):
        # Dimensions
        self.screen_width = 640
        self.screen_height = 480
        
        pygame.init()
        pygame.display.set_caption('Git Boom Visualizer')
        
        # Screen size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        texture = pygame.image.load('git_boom_visualizer/circle.png')
        self.particle_manager = ParticleManager(200, texture)


        # Fps
        self.clock = pygame.time.Clock()
        self.fps = 60 

        self.lock = Lock()
        self.boost_left = 0
    
    def load_font(self, path, size, bold=False):
        if not os.path.isfile(path):
            return
        font = pygame.font.Font(path, size)
        if bold: font.set_bold(True)
        return font

    def post(self):
        with self.lock:
            self.boost_left = 100
    
    def run(self):
        while True:
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break                   #   ... leave game loop

            if self.lock.acquire(False):
                if self.boost_left > 0:
                    self.boost_left -= 1

                self.lock.release()
           
            pygame.display.update()
            ms_elapsed = self.clock.tick(self.fps)
            self.particle_manager.update(ms_elapsed, self.boost_left * 5)

            self.screen.fill((0, 0, 0))
            self.particle_manager.draw(self.screen)


if __name__ == '__main__':
    visualizer = Visualizer()
    visualizer.run()
