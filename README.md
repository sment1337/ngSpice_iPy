# General info
This is a repository for an interface I want to write in ngSpice


Here is an example script that you can run in iPython to verify its working properly

```python
from importlib import reload
import ngInterfacer
reload(ngInterfacer)
from ngInterfacer import *
cir = circuit()
cir.getInstanceVal('ccouple')
cir.setInstanceVal('ccouple', 1e-12)
```
