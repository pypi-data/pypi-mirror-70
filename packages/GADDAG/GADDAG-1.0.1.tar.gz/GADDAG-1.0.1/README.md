# GADDAG

GADDAG is a Python wrapper around [cGADDAG](https://github.com/jorbas/cGADDAG).

A GADDAG data structure provides rapid word lookups for prefixes,
suffixes and substrings, making it ideal for use in applications such as
move generation in word games such as
[Scrabble](https://en.wikipedia.org/wiki/Scrabble).

Basic usage:

```python
>>> import gaddag
>>> words = ["foo", "bar", "foobar", "baz"]
>>> gdg = gaddag.GADDAG(words)
>>> "foo" in gdg
True
>>> "bor" in gdg
False
>>> gdg.contains("ba")
['bar', 'foobar', 'baz']
```

GADDAG currently only supports the ASCII alphabet.

## Installation

From [PyPI](https://pypi.python.org/pypi/GADDAG):

`pip install gaddag`

## Documentation

Documentaion is available in the `docs` directory, or rendered at
<http://gaddag.readthedocs.io>.

## License

Licensed under the MIT License, see
[LICENSE](https://github.com/jorbas/GADDAG/blob/master/LICENSE).
