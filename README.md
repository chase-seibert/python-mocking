# Python Mock Cookbook

The python [mock](https://pypi.python.org/pypi/mock) library is one of the awesome things about working in Python. No matter what code you're unit testing, it's possible to mock out various pieces with very little test code. That being said, it's sometimes difficult to figure out the exact syntax for your situation. I attribute this to the nature of how you apply the mocks. Sometimes it feel like you're TODO.

The [official documentation](https://docs.python.org/3/library/unittest.mock.html) is comprehensive, but I find it somewhat hard to find what you're looking for. I recommend their [examples doc](http://www.voidspace.org.uk/python/mock/examples.html).

This post is a write-up of my own personal usage.

# Big Upfront Caveat

The biggest mistake people make with mock is something out in the wrong place. *You always need to mock the thing where it's imported TO, not where it's imported FROM.* Translation: if you're importing `from foo import bar` into a package `bat.baz`, you need to mock it as `@mock.patch('bat.baz.bar')`. This can be confusing if you think you should be mocking it where it's defined, not where it's used.

# Setup

For all these sections, assume we're in a package called `myapp`. The code you're testing in a module at `myapp.app` and the definition of the objects that you're mocking is imported there from `myapp.lib`.

*app.py*

```python
```

*lib.py*

```python
```

# Constants

The easiest things to mock out are constants.

```python
@mock.patch('myapp.app.MAX_ITEMS', 7)
def test_constant(self):
    ...
```

# Functions

For functions, you will commonly need to specify a return value, check if they were called, and with what values.

```python
@mock.patch('myapp.app.get_first_name')
def test_function(self, mock_get_first_name):
    mock_get_first_name.return_value = 'Bat'
    ...
    mock_get_first_name.assert_called()
    mock_get_first_name.assert_called_once_with('baz')
```

# Methods

Mocking a method on a class is just like mocking a function, you just reference it through the class name.

```python
@mock.patch('myapp.app.Car.get_make')
def test_method(self, mock_get_make):
    mock_get_make.return_value = 'Ford'
    ...
    mock_get_make.assert_called()
```

# Properties

These are just special methods on a class with the `@property` decorator. Now we're starting to get tricky.

```python
@mock.patch('myapp.app.Car.wheels', new_callable=mock.PropertyMock)
def test_property(self, mock_wheels):
    mock_wheels.return_value = 2
    ...
```

# Entire classes

What if you want to swap out an entire class implementation? No problem! The key is that the `return_value` should be a new instance of the class.

```python
@mock.patch('myapp.app.Car')
def test_class(self, mock_car):

    class NewCar(object):

        def get_make(self):
            return 'Audi'

        @property
        def wheels(self):
            return 6

    mock_car.return_value = NewCar()
    ...
```

# Class Methods

What about a `@classmethod` on a class? It's the same as a method.

```python
@mock.patch('myapp.app.Car.for_make')
def test_classmethod(self, mock_for_make):
    new_car = Car()
    new_car.make = 'Chevy'
    mock_for_make.return_value = new_car
    ...
```

# Static Methods

Static methods are the same as class methods.

```python
@mock.patch('myapp.app.Car.roll_call')
def test_classmethod(self, mock_get_roll_call):
    mock_get_roll_call.return_value = [Car('Ford'), ]
    ...
```

# Decorators & Context Managers

Decorators are a tough one. They are defined at import time, and are thus diffucult to re-define as a mock. Your best bet is to create a function for the body of the decorator, and mock that.

Context managers are more do-able, but tricky.

```python
@mock.patch('myapp.app.open_car')
def test_context_manager(self, mock_open_car):

    def enter_car(car):
        pass

    mock_open_car.return_value.__enter__ = enter_car

    ...
```

# Bonus - Mocking All Tests in a Suite

San you have a certain mock that you want to apply to all tests in a TestCase class. You have two options. You can apply the patch in the `setUp` and un-apply the patch in `tearDown`, or you can over-ride `run`.

```python
def run(self, result=None):
    with mock.patch('myapp.app.foo') as foo:
        self.foo = foo
        super(MyTestCase, self).run(result)
```
