from func_timeout import FunctionTimedOut
from threading import Thread


def decode(str):
    if type(str) is bytes:
        return str.decode("ISO-8859-1")
    return str


def encode(str):
    if type(str) is not bytes:
        try:
            return str.encode("ISO-8859-1")
        except:
            return str
    return str


def time_out(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            return result
        except FunctionTimedOut:
            print('timeout')
            return []

    return wrapper

"""
changeunsignednumber:公共方法
将四个字节的无符号数换算为一个十进制数
"""
def unsignnumconv(forcebyte, thirdbyte, secondbyte, firstbyte):
    return forcebyte+2**8*thirdbyte+2**16*secondbyte+2**24*firstbyte

"""
changenumber:公共方法
将四个字节的有符号数换算为一个十进制数
"""
def signnumconv(forcebyte, thirdbyte, secondbyte, firstbyte):
    number = forcebyte + 2 ** 8 * thirdbyte + 2 ** 16 * secondbyte + 2 ** 24 * firstbyte
    if 2 ** 31 < number:
        lon = (-1) * number
    return number

# 异步线程装饰器
def asyncfun(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
