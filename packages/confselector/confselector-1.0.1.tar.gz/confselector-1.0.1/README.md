
config selector

```pycon
>>> import os
>>> SELFDIR = os.path.dirname(os.path.abspath('.'))  # or : SELFDIR = os.path.dirname(os.path.abspath(__file__))
>>> PROJECTDIR = os.path.dirname(SELFDIR)
>>> 
>>> from confselector import ConfSelector
>>> ConfSelector.configure([PROJECTDIR, os.path.join(PROJECTDIR, 'config'), os.path.join(PROJECTDIR, 'conf'), SELFDIR, ])
>>> 
>>> pyfile, configobj = ConfSelector.selected('-dev')
>>> print(pyfile, configobj)
>>> 
>>> pyfile, configobj = ConfSelector.selected('-prod')
>>> print(pyfile, configobj)
>>> 
>>> pyfile, configobj = ConfSelector.selected('')
>>> print(pyfile, configobj)
>>> 
```

---------------------------------------------------------------------
