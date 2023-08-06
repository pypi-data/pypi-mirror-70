# EMS logging
## Setup

Either import this as a git submodule package (for development) and `import emslogging`, or simply import the [ems-logging](https://pypi.org/project/ems-logging/) library from pypi and use the python get logger:

```Python3
import emslogging
import logging
logger = logging.getLogger("Zipping")
```

Log level can be set with env variable `EMS_LOG_LEVEL` using the python logging library levels, e.g. `INFO`, `DEBUG`, etc.