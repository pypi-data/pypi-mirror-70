
logger holder

```pycon
>>> import logging
>>> import os
>>> SELFDIR = os.path.dirname(os.path.abspath('.'))  # or : SELFDIR = os.path.dirname(os.path.abspath(__file__))
>>> PROJECTDIR = os.path.dirname(SELFDIR)
>>> 
>>> from loggerholder import LoggerHolder
>>> logargs = ('logs/app.log', 'h', '%(asctime)s %(process)d %(thread)d %(levelname)s: %(message)s', logging.DEBUG, PROJECTDIR)
>>> logger = LoggerHolder.holded(logargs)
>>> print(logger)
>>> 
```

---------------------------------------------------------------------
