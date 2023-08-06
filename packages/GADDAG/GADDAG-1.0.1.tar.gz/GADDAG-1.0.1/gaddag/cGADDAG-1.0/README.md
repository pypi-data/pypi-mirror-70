# cGADDAG

A C implementation of a semi-minimized [GADDAG][gaddag], described in '[A
Faster Scrabble Move Generation Algorithm][paper]' (Gordon, 1994).

A GADDAG data structure provides rapid word lookups for prefixes,
suffixes and substrings, making it ideal for use in applications such as
[Scrabble][scrabble] move generation.

cGADDAG currently only supports the lowercase English alphabet.

## Dependencies

cGADDAG optionally depends on [zlib][zlib] for saving/loading compressed
GADDAGs to/from file.

## Building

cGADDAG can be built as either a static or shared library. To build it as a
static library, run:

```bash
$ make
```

To build it as a shared library, run:

```bash
$ make SHARED=y
```

By default, compression via zlib is included. If you would rather not have this
feature, run:

```bash
$ make ZLIB=n [SHARED=y]
```

## Usage

For an example of how to use cGADDAG, see `src/example.c`.

This example can be built by running:

```bash
$ make example [ZLIB=n]
```

```bash
$ ./example
Created a new GADDAG
Added "CARE" to GADDAG
Added "CAR" to GADDAG
Added "BAR" to GADDAG

Node capacity: 100
Total words: 3
Total nodes: 17
Total edges: 19

Contains CARE: 1
Contains CAR: 1
Contains FOO: 0

Finding words ending with 'AR'
  car
  bar

Finding words starting with 'CAR'
  care
  car

Finding words containing 'AR'
  care
  car
  bar

Edges from root (5): abcer
Letter set for root -> R -> A (2): bc

Saving GADDAG to 'example.gdg': 11216
Saving compressed GADDAG to 'example.gdg.gz': 11216
```

## License

Licensed under the MIT License, see `LICENSE`.

[gaddag]: <https://en.wikipedia.org/wiki/GADDAG>
[paper]: <https://ericsink.com/downloads/faster-scrabble-gordon.pdf>
[scrabble]: <https://en.wikipedia.org/wiki/Scrabble>
[zlib]: <https://www.zlib.net>
