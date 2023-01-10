# cli-help-maker
Command Line Interface help message generator.

*The content is still work In progress, some bugs are present.*

This repo contains a CLI to create simulated help messages with the positions annotated
of the commands, arguments and options. Its created as a separated package, but its only intended use is to generate datasets to be usd in [helpner-core](https://github.com/plaguss/helpner-core), which does the work for [helpner](https://github.com/plaguss/helpner).

## What range of help messages covers?

For the moment, it indents to recreate messages like those found in the examples of [docopt-ng]
(https://github.com/jazzband/docopt-ng).
This should cover CLI apps created in python using for example [argparse](https://docs.python.org/3/library/argparse.html), [click](https://click.palletsprojects.com/en/8.1.x/) or [typer](https://typer.tiangolo.com/)*.

*[typer](https://typer.tiangolo.com/) when prettefied via `rich` its not in the scope.*

## Installation

(Once in PyPI):

`pip install cli-help-maker`

This creates the following CLI:

```console
❯ cli-help-maker --help
                                                                                                
 Usage: cli-help-maker [OPTIONS] INPUT_PATH [OUTPUT_PATH]                                       
                                                                                                
 Function to generate a dataset of cli help messages from a .yaml file with the info.           
 A folder will be generated containing two jsonl files:                                         
 - arguments.jsonl:     Contains the arguments that were generated, these can be associated to  
 each     help message for further analysis.                                                    
 - dataset.jsonl:     A dataset of help messages with annotations.                              
                                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────╮
│ *    input_path       FILE           Path pointing to the .yaml file. [default: None]        │
│                                      [required]                                              │
│      output_path      [OUTPUT_PATH]  Dirname of the output path. If not given, creates a     │
│                                      directory with the version number                       │
│                                      [default: None]                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the      │
│                                                              specified shell.                │
│                                                              [default: None]                 │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the         │
│                                                              specified shell, to copy it or  │
│                                                              customize the installation.     │
│                                                              [default: None]                 │
│ --help                                                       Show this message and exit.     │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Development

TBD

## Examples

The folder [examples](https://github.com/plaguss/cli-help-maker/tree/main/examples) contains a rough recreation of some of the examples found in `docopt-ng` repo, to see an example, run any of them, for example:

```bash
python examples/arguments_example_like.py
```

This would create a random help message with a layout similar to the one found in [docopt-ng](https://github.com/jazzband/docopt-ng/blob/master/examples/arguments_example.py) (approximately).
