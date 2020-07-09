from _util import ClickAction, MouseButton

import sys
if sys.platform.startswith('win'):   
    from windows._mouse import click, move     
elif sys.platform.startswith('darwin'):
    from mac._mouse import click, move
else:
    from linux._mouse import click, move

