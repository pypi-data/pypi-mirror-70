# lets-debug

## Install

`pip install lets-debug`

## Tools

You will find useful tools for debugging in Python with this package.

The main feature here is `terminal` variable, an istance of `_Terminal` class that allows you to print anything on terminal using different colors. Some methods of this class are similar to JavaScript `Console` native class.

Another useful tool for debugging code is `stopwatch` decorator method from `DecoratorTools` class. It allows you to verify how much longer is the waiting time for any function.

```python
from lets_debug import terminal, DecoratorTools as tools

@tools.stopwatch
def greeting():
    terminal.count('Greeting function')

greeting()
```

The example code above will give you an output like this:

```
Greeting function: 1
Waiting time for greeting: 0.04291534423828125
```

Some ideas of this package come from other languages, like Java.

```python
class Person:

    def __init__(self, is_alive=True):
        self.is_alive = is_alive

    def code(self):
        pass

class Programmer(Person):

    def __init__(self, is_alive):
        super().__init__(is_alive)

        if self.is_alive:
            self.code()

    @tools.override(get_error=True) # If code() does not exist on Person class an Exception occurs
    def code(self):
        terminal.log('Keep coding :)')
```

Now, explore the tools of this package and feel free to colaborate with your best ideas!