# Windows setup guide


Following is a tutorial on how to setup the software and harwdware regarding the installation.


## Resources

setup sending midi signals https://www.gorillasun.de/blog/midi-signals-from-python-to-ableton-live/

## Software

Python 3.10 along with Poetry is required

in the project folder:
```bash
poetry install
poetry env use <path to python3.10 executable>
poetry shell
pip install rerun-sdk
```

## Instrumento + midi setup

Install https://www.tobias-erichsen.de/software/loopmidi.html and create virtual midi device

