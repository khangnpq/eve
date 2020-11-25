#coding:utf8
import inspect, sys
from eve import settings_dev
IS_DEV = True #if platform.platform().find('Linux') == -1 else False
print('IS_DEV: ', IS_DEV)
clsmembers = inspect.getmodule(sys.modules[__name__])
if IS_DEV:
    clsmembers.__dict__.update(settings_dev.__dict__)
else:
    clsmembers.__dict__.update(settings_online.__dict__)
