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
    def __init__(self, particle_count, texture):
        self.particle_count = particle_count
        self.texture = texture

        self.rand = Random()
        self.particles = []
        for i in range(particle_count):
            self.particles.append(self.random_particle())

    def update(self, ms_elapsed, boost):
        self.particles = filter(lambda p: p.update(ms_elapsed),
                                self.particles)

        for i in range(self.particle_count - len(self.particles) + boost):
            self.particles.append(self.random_particle())

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen, self.texture)

    def random_particle(self):
        randint = self.rand.randint
        return Particle(randint(100, 500), randint(470, 480),
                        self.rand.uniform(-0.3, 0.3) - pi / 2,
                        randint(1, 5), randint(5, 60), 100)
