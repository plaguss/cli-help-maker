# cli-help-maker
Command Line Interface help message generator.

This project is an attempt to make a *help message* generator for a cli program, what you would obtain from calling `program -h` or `program --help`, like with `git --help`.


## What does it contain?

- [templates](templates):

    Contains jinja templates for the help message generates by a framework. i.e. `docopt-ng.jinja` is a template for the help message
    that would be obtained from a cli generated with [docopt.ng](https://github.com/jazzband/docopt-ng).

Using as an example `docopt-ng.jinja`. The following corresponds to the help message of an app called *Naval Fate*:

```console
Naval Fate.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored|--drifting]
  naval_fate.py -h | --help
  naval_fate.py --version
Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
```

The content can be generated from the following template:

```console
a
```
