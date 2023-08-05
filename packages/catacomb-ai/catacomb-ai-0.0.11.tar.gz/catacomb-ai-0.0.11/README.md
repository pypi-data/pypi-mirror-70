# Catacomb
> Deploy models that you can trust.

Catacomb is a platform that hosts machine learning models so that anybody can interact with them.

## Installation
Catacomb's Python library can be installed from the PyPi registry:

```
pip install catacomb-ai
```

To test installation, run `catacomb`:

```
Usage: catacomb [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init
```

## Usage

Catacomb expects a `system.py` file that implements the `System` class, including overriding
the `output` method and providing appropriate type annotations in `__init__` through the `format` method:

```python
import catacomb
from catacomb import Types

class MyModel(catacomb.System):
    def __init__(self):
        # Set system type annotations
        self.format(Types.NUMBER, Types.NUMBER)
        # Finish other system setup
        self.variable = 42

    def output(self, input_object):
        # Performing inference and returning a prediction
        return input_object * self.variable
```

The typing annotation allows Catacomb to auto-generate a UI for the system/model, in addition to performing
predictions over HTTP.

## License
MIT