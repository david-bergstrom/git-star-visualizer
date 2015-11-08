import pygame

from random import Random
from math import cos, sin, pi


def shift_center(pos, image):
    shift = (- image.get_width() / 2.0, - image.get_height() / 2.0)
    return map(sum, zip(pos, shift))


# From: http://everything2.com/title/Fire+Color+Pallet
def get_fire_color(intensity):
    r = min(intensity, 85) * 3
    intensity = max(intensity-85, 0)
    g = min(intensity, 85) * 3
    intensity = max(intensity-85, 0)
    b = min(intensity, 85) * 3
    return r, g, b


class Particle:
    def __init__(self, x, y, angle, angular_velocity, ttl):
        self.x = x
        self.y = y
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.ttl = ttl

        self.time_lived = 0

    # Updates the particle and returns whether it needs replacing
    def update(self, time):
        self.ttl -= time
        self.time_lived += time
        self.x += self.angular_velocity * cos(self.angle)
        self.y += self.angular_velocity * sin(self.angle)

        return self.ttl > 0

    def get_pos(self):
        return int(self.x), int(self.y)

    def draw(self, screen):
        intensity = 255 * (1 - min(1, self.time_lived / 1000.0))
        pygame.draw.circle(screen, get_fire_color(intensity), self.get_pos(), 8)


class ParticleManager:
    def __init__(self, particle_count, screen_width, screen_height):
        self.particle_count = particle_count
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
        x = self.rand.randint(400, self.screen_width - 400)
        y = self.rand.randint(self.screen_height - 20, self.screen_height)
        angle = self.rand.uniform(-0.3, 0.3) - pi / 2
        angular_velocity = self.rand.randint(1, 5)
        ttl = self.rand.randint(80, 1000)

        return Particle(x, y, angle, angular_velocity, ttl)
