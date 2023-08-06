"""
Entrypoint module, in case you use `python -mdownload_accelerator`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

import argh

from download_accelerator.cli import download

parser = argh.ArghParser()
parser.add_commands([download])

# dispatching:

if __name__ == '__main__':
    parser.dispatch()
