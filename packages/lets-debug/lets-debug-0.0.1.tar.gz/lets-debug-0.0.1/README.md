# lets-debug

Inside `debug.py` you will find useful tools for debugging in Python.

The main feature of this file is `terminal` variable, an istance of `_Terminal` class that allows you to print anything on terminal with different colors. Some methods of this class are similar to JavaScript `Console` native class.

Another useful tool for debugging is the `stopwatch` decorator method from `DecoratorTools` class. It allows you to verify how much longer is the waiting time for any function.

```
from lets_debug import terminal, DecoratorTools as tools

@tools.stopwatch
def greeting():
    terminal.count('Greeting function')

greeting()
```

The example code above will give an output like this:

```
Greeting function: 1
Waiting time for greeting: 0.04291534423828125
```
