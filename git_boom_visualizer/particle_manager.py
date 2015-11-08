from random import Random
from math import cos, sin, pi


def shift_center(pos, image):
    shift = (- image.get_width() / 2.0, - image.get_height() / 2.0)
    return map(sum, zip(pos, shift))


class Particle:
    def __init__(self, x, y, angle, angular_velocity, ttl, size):
        self.x = x
        self.y = y
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.ttl = ttl
        self.size = size

    # Updates the particle and returns whether it needs replacing
    # TODO: Use time
    def update(self, time):
        self.ttl -= 1
        self.x += self.angular_velocity * cos(self.angle)
        self.y += self.angular_velocity * sin(self.angle)

        return self.ttl > 0

    def get_pos(self):
        return int(self.x), int(self.y)

    def draw(self, screen, texture):
        pos = self.get_pos()
        screen.blit(texture, shift_center(pos, texture))


class ParticleManager:
    def __init__(self, particle_count, texture, screen_width, screen_height):
        self.particle_count = particle_count
        self.texture = texture
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rand = Random()
        self.particles = []
        for i in range(particle_count):
            self.particles.append(self.random_particle())

    def update(self, ms_elapsed, boost):
        self.particles = filter(lambda p: p.update(ms_elapsed),
                                self.particles)

        for _ in range(self.particle_count - len(self.particles) + boost):
            self.particles.append(self.random_particle())

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen, self.texture)

    def random_particle(self):
        x = self.rand.randint(100, self.screen_width - 100)
        y = self.rand.randint(self.screen_height - 20, self.screen_height)
        angle = self.rand.uniform(-0.3, 0.3) - pi / 2
        angular_velocity = self.rand.randint(1, 5)
        ttl = self.rand.randint(5, 60)
        size = 100

        return Particle(x, y, angle, angular_velocity, ttl, size)
