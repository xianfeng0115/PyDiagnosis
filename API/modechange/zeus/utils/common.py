
import time

def wait(call_back, ex_msg='', timeout=30, sleeptime = 1, *args, **kwargs):
    if call_back == None:
        raise Exception('The call_back function could not be none.')
        
    start = time.clock()    
    while not call_back(*args, **kwargs):
        time.sleep(sleeptime)  
        _timeout = time.clock() - start >= timeout
        if _timeout:
            raise Exception('Timeout(%d): %s' % (timeout, ex_msg))