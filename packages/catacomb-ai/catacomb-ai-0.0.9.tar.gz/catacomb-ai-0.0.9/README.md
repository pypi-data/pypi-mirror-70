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
the `output` method (which returns the system/model's prediction) and providing appropriate type decorations:

```python
from catacomb.systems import Types, System

class MyModel(System):
    def __init__(self):
        print('Doing some model setup here!')

    @System.input_type(Types.TEXT)
    @System.output_type(Types.NUMBER)
    def output(self, input_):
        print('Performing inference and returning a prediction!')
        return 42
```

The typing decorators allows Catacomb to auto-generate a UI for the system/model, in addition to performing
predictions over HTTP.

## License
MIT