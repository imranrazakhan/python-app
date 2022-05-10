from runpy import run_path


# read the program version from version.py (without loading the module)
__version__ = run_path('src/hello-flask/version.py')['__version__']


