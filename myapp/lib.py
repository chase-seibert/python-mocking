from contextlib import contextmanager


MAX_ITEMS = 10


def get_first_name(arg):
    return arg or "Foo"


class Car(object):

    def __init__(self, make=None):
        self.make = make
        self.closed = False

    @classmethod
    def for_make(cls, make):
        car = cls()
        car.make = make
        return car

    def get_make(self):
        return self.make

    @property
    def wheels(self):
        return 4

    @staticmethod
    def roll_call():
        return [Car('Ford'), Car('Chevy'), Car('BMW'), Car('Audi')]

    def close(self):
        self.closed = True

    def __repr__(self):
        return '<Car: %s>' % self.make

    def __eq__(self, other):
        return self.make == other.make


@contextmanager
def open_car(car):
    yield car
    car.close()
