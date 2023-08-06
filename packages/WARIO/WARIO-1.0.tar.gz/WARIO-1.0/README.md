# WARIO Pipeline Backend

This library provides the backend to the WARIO pipeline development system. It can be used with any compatable pipeline file (see [WARIO Editor](https://github.com/McMasterRS/WARIO-Editor/)) and allows for the development of custom interfaces that can be directly linked to the pipeline code.

## Installation

```bash
pip install wario
```

### Dependancies

Python 3.6
PyQt5
blinker

## Usage

To use WARIO independant of a frontend

```python
from wario import PipelineThread


pipeline = PipelineThread(filename)
pipeline.start()

```

WARIO pipelines can also be linked to interfaces through the use of blinker signals. For an example of this, see the [RunPipeline interface file in the WARIO Editor](https://github.com/McMasterRS/WARIO-Editor/blob/master/RunPipeline.py)

## Contributers

Oliver Cook
Thomas Mudway
Ron Harwood