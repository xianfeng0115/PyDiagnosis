
import sys

if sys.platform.startswith('win'):
    from windows._keyboard import sendkeys, keydown, keyup
elif sys.platform.startswith('darwin'):
    from mac._keyboard import sendkeys, keydown, keyup
else:
    from linux._keyboard import sendkeys, keydown, keyup
    