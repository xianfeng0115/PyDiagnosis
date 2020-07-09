
import time, re
from _util import get_root, get_parent, get_firstchild, get_lastchild, get_nextsibling, get_prevsibling, get_children
from zeus.gui.util import decode, QueryScope
#from zeus.gui.exceptions import TimeoutError, ElementNotFoundError


def match_props(host, criteria):
    for name, value in criteria.iteritems():            
        if not match_prop(host, name, value):
            return False
    return True

def match_prop(host, name, value):
    actual = getattr(host, name, None)    
    if isinstance(value, basestring):
        value = decode(value)
        if value[0] == '~':                
            return regular_exp(actual, value[1:])
        elif value[0] == '*':
            return contains(actual, value[1:])
        elif value[0] == '\\':
            value = value[1:]
        else:
            pass
    return equals(actual, value)

def regular_exp(actual, pattern):    
    return None != actual and None != re.match(pattern, actual)

def equals(actual, expected):
    return None != actual and expected == actual

def contains(actual, expected):    
    return actual.find(expected) > -1
    

class Finder(object):
    
    def root(self):
        return get_root()
    
    def parent(self, host):
        return get_parent(host)
    
    def firstchild(self, host):
        return get_firstchild(host)
    
    def lastchild(self, host):
        return get_lastchild(host)
    
    def nextsibling(self, host):
        return get_nextsibling(host)
    
    def prevsibling(self, host):
        return get_prevsibling(host)
    
    def children(self, host):
        return get_children(host)
    
    def find_all(self, qid):        
        start = qid.start
        cond = qid.criteria.pop()        
        for con in qid.criteria:
            start = self._find_by_condition(start, con)
                
        strategy = None
        if cond.scope == QueryScope.Children:
            strategy = ChildrenStrategy()
        elif cond.scope == QueryScope.Descendants:
            strategy = DescendantsStrategy()
        elif cond.scope == QueryScope.Ancestors:
            strategy = AncestorsStrategy()
        elif cond.scope == QueryScope.Siblings:
            strategy = SiblingsStrategy()
        else:
            pass
        return strategy.find_all(start, cond.timeout, cond.condition)
        
    def find(self, qid):
        found = qid.start
        for con in qid.criteria:
            found = self._find_by_condition(found, con)
        return found
    
    def _find_by_condition(self, start, con):        
        time.sleep(con.delay)        
        strategy = None
        if con.scope == QueryScope.Children:
            strategy = ChildrenStrategy()
        elif con.scope == QueryScope.Descendants:
            strategy = DescendantsStrategy()
        elif con.scope == QueryScope.Ancestors:
            strategy = AncestorsStrategy()
        elif con.scope == QueryScope.Siblings:
            strategy = SiblingsStrategy()
        else:
            pass
        return strategy.find(start, con.index, con.timeout, con.condition)


class FindStrategy(object):
    def __init__(self):
        pass    
    
    def verify(self, host, criteria):
        return match_props(host, criteria)
    
    def find_all(self, *args):
        pass
    
    def find(self, *args):
        pass

class SiblingsStrategy(FindStrategy):
    def find(self, *args):
        host, index, timeout, criteria = args        
        starttime = time.clock()   
        found = host.nextsibling()
        while found is not None:
            if time.clock() - starttime - timeout > 0:
                raise Exception('TimeoutError has benn occurred. - %d sec(s)' % timeout)
            if self.verify(found, criteria):
                if index < 1:
                    return found
                index -= 1                 
            found = found.nextsibling()
        
        found = host.prevsibling()
        while found is not None:
            if time.clock() - starttime - timeout > 0:
                raise Exception('TimeoutError has benn occurred. - %d sec(s)' % timeout)
            if self.verify(found, criteria):
                if index < 1:
                    return found
                index -= 1
            found = found.prevsibling() 
        
        raise Exception('Element not found with %s' % repr(criteria))
    
    def find_all(self, *args):
        host, timeout, criteria = args        
        #starttime = time.clock()        
        found = host.nextsibling()
        while found is not None:
            #if time.clock() - starttime - timeout > 0:
            #    raise TimeoutError(timeout)
            if self.verify(found, criteria):
                yield found
            found = found.nextsibling()
        
        found = host.prevsibling()
        while found is not None:
            #===================================================================
            # if time.clock() - starttime - timeout > 0:
            #    raise TimeoutError(timeout)
            #===================================================================
            if self.verify(found, criteria):
                yield found
            found = found.prevsibling()
        
        #raise ElementNotFoundError(criteria)

class AncestorsStrategy(FindStrategy):
    def find(self, *args):
        host, index, timeout, criteria = args        
        starttime = time.clock()        
        parent = host.parent()
        while parent is not None:
            if time.clock() - starttime - timeout > 0:
                raise Exception('TimeoutError has benn occurred. - %d sec(s)' % timeout)
            if self.verify(parent, criteria):
                if index < 1:
                    return parent
                index -= 1            
            parent = parent.parent()
        raise Exception('Element not found with %s' % repr(criteria))
    
    def find_all(self, *args):
        host, timeout, criteria = args
        
        #starttime = time.clock()
        
        parent = host.parent()
        while parent is not None:
            #if time.clock() - starttime - timeout > 0:
            #    raise TimeoutError(timeout)    
            if self.verify(parent, criteria):
                yield parent            
            parent = parent.parent()
        #raise ElementNotFoundError(criteria)

class DescendantsStrategy(FindStrategy):
    def find(self, *args):
        host, index, timeout, criteria = args
        
        starttime = time.clock()
        import Queue
        queue = Queue.Queue()
        queue.put(host)
        while queue.qsize()> 0:
            child = queue.get()
            child = child.firstchild()
            while child != None:
                queue.put(child)                
                if self.verify(child, criteria):
                    if index < 1:
                        return child
                    index -= 1
                if time.clock() - starttime - timeout > 0:
                    raise Exception('TimeoutError has benn occurred. - %d sec(s)' % timeout)
                child = child.nextsibling()
        raise Exception('Element not found with %s' % repr(criteria))
    
    def find_all(self, *args):
        host, timeout, criteria = args
        
        starttime = time.clock()
        import Queue
        queue = Queue.Queue()
        queue.put(host)
        while queue.qsize()> 0:
            child = queue.get()
            child = child.firstchild()
            while child != None:
                queue.put(child)
                if self.verify(child, criteria):
                    yield child
                if time.clock() - starttime - timeout > 0:
                    raise Exception('TimeoutError has benn occurred. - %d sec(s)' % timeout)
                child = child.nextsibling()
        #raise ElementNotFoundError(criteria)

class ChildrenStrategy(FindStrategy):
    def find(self, *args):
        host, index, timeout, criteria = args        
        starttime = time.clock()
        
        child = host.firstchild()
        while child != None:
            if time.clock() - starttime - timeout > 0:
                raise Exception('TimeoutError has benn occurred. - %d sec(s)' % timeout)
            if self.verify(child, criteria):
                if index < 1:
                    return child
                index -= 1
            child = child.nextsibling() 
        raise Exception('Element not found with %s' % repr(criteria))
    
    def find_all(self, *args):
        host, timeout, criteria = args        
        #starttime = time.clock()     
        child = host.firstchild()
        while child != None:
            #if time.clock() - starttime - timeout > 0:
            #    raise TimeoutError(timeout)
            if self.verify(child, criteria):
                yield child
            child = child.nextsibling()
        #raise ElementNotFoundError(criteria)


        
        