from contextlib import contextmanager
import mock
from unittest import TestCase

from myapp.app import get_max_items, get_full_name, get_car_make, get_car_wheels, get_roll_call, \
    close_car
from myapp.lib import Car


class MyTests(TestCase):

    @mock.patch('myapp.app.MAX_ITEMS', 7)
    def test_constant(self):
        self.assertEquals(get_max_items(), 7)

    @mock.patch('myapp.app.get_first_name')
    def test_function(self, mock_get_first_name):
        mock_get_first_name.return_value = 'Bat'
        self.assertEquals(get_full_name('baz'), 'Bat Bar')
        mock_get_first_name.assert_called()
        mock_get_first_name.assert_called_once_with('baz')

    @mock.patch('myapp.app.Car.get_make')
    def test_method(self, mock_get_make):
        mock_get_make.return_value = 'Ford'
        self.assertEquals(get_car_make(), 'Ford')
        mock_get_make.assert_called()

    @mock.patch('myapp.app.Car.wheels', new_callable=mock.PropertyMock)
    def test_property(self, mock_wheels):
        mock_wheels.return_value = 2
        self.assertEquals(get_car_wheels(), 2)

    @mock.patch('myapp.app.Car')
    def test_class(self, mock_car):

        class NewCar(object):

            def get_make(self):
                return 'Audi'

            @property
            def wheels(self):
                return 6

        mock_car.return_value = NewCar()
        self.assertEquals(get_car_make(), 'Audi')
        self.assertEquals(get_car_wheels(), 6)

    @mock.patch('myapp.app.Car.roll_call')
    def test_classmethod(self, mock_get_roll_call):
        mock_get_roll_call.return_value = [Car('Ford'), ]
        self.assertEquals(get_roll_call(), [Car('Ford'), ])

    @mock.patch('myapp.app.open_car')
    def test_context_manager(self, mock_open_car):

        car = Car()
        car.closed = 'Foo'

        def enter_car(car):
            car.closed = 'Bar'
            return car

        mock_open_car.return_value.__enter__ = enter_car
        #mock_open_car.return_value.__exit__ = exit_car

        states = close_car(car)
        self.assertEquals(states, ['Bar', 'Bar'])
