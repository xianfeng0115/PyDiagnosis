import _uia, time
from zeus.gui.util import State, Role
from zeus.osinput import keyboard
from zeus.osinput import mouse
from zeus.gui.util import QueryId
from _finder import Finder
finder = Finder()

__all__ = ['Element']

class TypedElement(object):
        
    def Element(self, **criteria):
        return Element(self.find(**criteria))
         
    def Pane(self, **criteria):
        criteria['role'] = Role.Pane
        return self.Element(**criteria)
    
    def Window(self, **criteria):
        criteria['role'] = Role.Window
        return self.Element(**criteria)
    
    def Button(self, **criteria):
        criteria['role'] = Role.Button
        return self.Element(**criteria)
    
    def Edit(self, **criteria):
        criteria['role'] = Role.Edit        
        return self.Element(**criteria)
    
    def Text(self, **criteria):
        criteria['role'] = Role.Text        
        return self.Element(**criteria)
    
    def ProcessBar(self, **criteria):
        criteria['role'] = Role.ProcessBar
        return self.Element(**criteria)
    
    def Menu(self, **criteria):
        criteria['role'] = Role.Menu        
        return self.Element(**criteria)
    
    def MenuItem(self, **criteria):
        criteria['role'] = Role.MenuItem        
        return self.Element(**criteria)
    
    def List(self, **criteria):
        criteria['role'] = Role.List        
        return self.Element(**criteria)
    
    def ListItem(self, **criteria):
        criteria['role'] = Role.ListItem        
        return self.Element(**criteria)
    
    def TitleBar(self, **criteria):
        criteria['role'] = Role.TitleBar        
        return self.Element(**criteria)
    
    def ToolBar(self, **criteria):
        criteria['role'] = Role.ToolBar        
        return self.Element(**criteria)
    
    def Tooltip(self, **criteria):
        criteria['role'] = Role.Tooltip        
        return self.Element(**criteria)
    
    def CheckBox(self, **criteria):
        criteria['role'] = Role.CheckBox        
        return self.Element(**criteria)
    
    def ComboBox(self, **criteria):
        criteria['role'] = Role.ComboBox        
        return self.Element(**criteria)
    
    def Hyperlink(self, **criteria):
        criteria['role'] = Role.Hyperlink
        return self.Element(**criteria)
    
    def Image(self, **criteria):
        criteria['role'] = Role.Image        
        return self.Element(**criteria)
    
    def RadioButton(self, **criteria):
        criteria['role'] = Role.RadioButton        
        return self.Element(**criteria)
    
    def Tree(self, **criteria):
        criteria['role'] = Role.Tree        
        return self.Element(**criteria)
    
    def TreeItem(self, **criteria):
        criteria['role'] = Role.TreeItem        
        return self.Element(**criteria)
    
    def Slider(self, **criteria):
        criteria['role'] = Role.Slider        
        return self.Element(**criteria)
    
    def Grid(self, **criteria):
        criteria['role'] = Role.Grid        
        return self.Element(**criteria)
    
    def GridItem(self, **criteria):
        criteria['role'] = Role.GridItem        
        return self.Element(**criteria)
    
    def Group(self, **criteria):
        criteria['role'] = Role.Group        
        return self.Element(**criteria)
    
    def MenuBar(self, **criteria):
        criteria['role'] = Role.MenuBar        
        return self.Element(**criteria)
    
    def Spinner(self, **criteria):
        criteria['role'] = Role.Spinner        
        return self.Element(**criteria)
    
    def SplitButton(self, **criteria):
        criteria['role'] = Role.SplitButton       
        return self.Element(**criteria)
    
    def ScrollBar(self, **criteria):
        criteria['role'] = Role.ScrollBar        
        return self.Element(**criteria)
    
    def StatusBar(self, **criteria):
        criteria['role'] = Role.StatusBar        
        return self.Element(**criteria)
    
    def Tab(self, **criteria):
        criteria['role'] = Role.Tab        
        return self.Element(**criteria)
    
    def TabItem(self, **criteria):
        criteria['role'] = Role.TabItem        
        return self.Element(**criteria)
    
    def Table(self, **criteria):
        criteria['role'] = Role.Table        
        return self.Element(**criteria)
    
    def Thumb(self, **criteria):
        criteria['role'] = Role.Thumb        
        return self.Element(**criteria)

class WindowVisualState:
    Normal = _uia.WindowVisualState_Normal
    Maximized = _uia.WindowVisualState_Maximized
    Minimized = _uia.WindowVisualState_Minimized

class ExpandCollapseState:
    Collapsed = _uia.ExpandCollapseState_Collapsed
    Expanded = _uia.ExpandCollapseState_Expanded
    PartiallyExpanded = _uia.ExpandCollapseState_PartiallyExpanded
    LeafNode = _uia.ExpandCollapseState_LeafNode

class DockPosition:
    Top = _uia.DockPosition_Top
    Left = _uia.DockPosition_Left
    Bottom = _uia.DockPosition_Bottom
    Right = _uia.DockPosition_Right
    Fill = _uia.DockPosition_Fill
    Null = _uia.DockPosition_None

class ScrollAmount:
    LargeDecrement = _uia.ScrollAmount_LargeDecrement
    SmallDecrement = _uia.ScrollAmount_SmallDecrement
    NoAmount = _uia.ScrollAmount_NoAmount
    LargeIncrement = _uia.ScrollAmount_LargeIncrement
    SmallIncrement = _uia.ScrollAmount_SmallIncrement

class ToggleState:
    On = _uia.ToggleState_On
    Off = _uia.ToggleState_Off
    Indeterminate = _uia.ToggleState_Indeterminate


def root():
    return Element(finder.root())
    
def from_point(x, y):
    pass
    
def from_focus():
    pass


class Element(TypedElement):
    
    def __init__(self, host):
        self._host = getattr(host, '_host', host)
        self._props = ['rtid', 'id', 'name', 'classname', 'pid', 'location', 'visible', 'role', 'available'
                       , 'enabled', 'focused', 'focusable',
                       ]
    
    def find(self, **kwargs):
        trytimes = kwargs.pop('trytimes', 2)
        sleeptime = kwargs.pop('sleeptime', 1)
        qid = QueryId(self, criteria = None, **kwargs)
        while trytimes > 0:
            try:
                found = finder.find(qid)        
                return Element(found)       
            except:
                time.sleep(sleeptime)
                trytimes -=1
        raise Exception('Element not found. Conditions: %s' % str(kwargs))        
    
    def find_all(self, **kwargs):
        qid = QueryId(self, criteria = None, **kwargs)
        return [Element(found) for found in finder.find_all(qid)]    
        
    def all_properties(self):
        #self._props.sort()
        return self._props
    
    def get_property(self, name):
        if name in self._props:
            return getattr(self, name, None)
    
    def __navigate_to(self, direction, index):
        def func(element, direction):
            if direction == 'parent':
                return finder.parent(self._host)
            elif direction == 'fchild':
                return finder.firstchild(self._host)            
            elif direction == 'lchild':
                return finder.lastchild(self._host)            
            elif direction == 'nsibling':
                return finder.nextsibling(self._host)
            elif direction == 'psibling':             
                return finder.prevsibling(self._host)
            else:
                pass
        element = func(self, direction)
        while index > 0 and element != None:
            element = func(element, direction)
            index -= 1
        
        if element != None:
            return Element(element)
    
    def child(self, index):
        child = None
        if index < 0:
            count = -1
            child = finder.lastchild(self._host)
            while count > index and child != None:
                child = finder.prevsibling(child)
                count -= 1
        else:
            count = 0
            child = finder.firstchild(self._host)
            while count < index and child != None:
                child = finder.nextsibling(child)
                count += 1
        if child != None:
            return Element(child)        
    
    def parent(self, index = 0):
        return self.__navigate_to('parent', index)
    
    def firstchild(self, index = 0):
        return self.__navigate_to('fchild', index)
    
    def lastchild(self, index = 0):
        return self.__navigate_to('lchild', index)
    
    def nextsibling(self, index = 0):
        return self.__navigate_to('nsibling', index)
    
    def prevsibling(self, index = 0):
        return self.__navigate_to('psibling', index)
    
    def children(self):
        for child in finder.children(self._host):
            yield Element(child)
    
        
    @property
    def rtid(self):
        return self._host.get_rtid()
    
    @property
    def id(self):
        return self._host.get_id()
    
    @property
    def name(self):
        return self._host.get_name()    
    
    @property
    def classname(self):
        return self._host.get_classname()    
        
    @property
    def pid(self):
        return self._host.get_pid()
    
    @property
    def location(self):
        return self._host.get_location()
    
    @property
    def visible(self):
        return self._host.get_visible()
    
    @property
    def role(self):
        return self._host.get_role()
    
    @property
    def available(self):
        return self._host.get_available()
    
    @property
    def enabled(self):
        return self._host.get_enabled()
    
    @property
    def focused(self):
        return self._host.get_focused()
    
    @property
    def focusable(self):
        return self._host.get_focusable()            
    
    @property
    def is_password(self):
        return bool(self._host.get_password())
    
    def setfocus(self):
        if self.focusable:
            self._host.setfocus()
    
    def click(self):
        try:
            self._host.invoke.invoke()
        except:
            pass
            
    def mouseclick(self, x=0, y=0, btn=mouse.MouseButton.Left, act=mouse.ClickAction.Click):
        left, top, right, bottom = self.location
        px = (left + right) / 2 + x
        py = (top + bottom) / 2 + y
        mouse.click(px, py, btn, act)
    
    def mousemove(self, x=0, y=0):
        left, top, right, bottom = self.location
        px = (left + right) / 2 + x
        py = (top + bottom) / 2 + y 
        mouse.move(px, py)
    
    def sendkeys(self, keys):
        self.setfocus()
        keyboard.sendkeys(keys)
    
    def __pattern_get(self, pattern, attribute):
        p = self._host._pattern(pattern)
        if p != None:
            meth = getattr(p, 'get_'+attribute)
            return meth()
        
    
    def __pattern_set(self, pattern, attribute, *value):
        p = self._host._pattern(pattern)
        if p != None:
            meth = getattr(p, 'set_'+attribute)
            return meth(*value)
    
    def __pattern_call(self, pattern, method):
        p = self._host._pattern(pattern)
        if p != None:
            meth = getattr(p, method)
            return meth()
    
    @property
    def state(self):
        state = 0
        temp = self.__pattern_get('window', 'visualstate')
        if temp != None:
            if temp == WindowVisualState.Maximized:
                state |= State.Maximized
            elif state == WindowVisualState.Minimized:
                state |= State.Minimized
            else:
                state |= State.Normal
        
        temp = self.movable
        if temp != None and temp:
            state |= State.Movable
        
        temp = self.sizable
        if temp != None and temp:
            state |= State.Sizable
        
        temp = self.__pattern_get('toggle', 'togglestate')
        if temp != None:
            if temp == ToggleState.On:
                state |= State.ToggledOn
            elif temp == ToggleState.Off:
                state |= State.ToggledOff
            else:
                state |= State.IndeterminateToggled
        
        temp = self.__pattern_get('selectionitem', 'selected')
        if temp != None:
            if temp == 0b1:
                state |= State.Selected

        temp = self.__pattern_get('expcol', 'state')
        if temp != None:
            if temp == ExpandCollapseState.Collapsed:
                state |= State.Collapsed
            elif temp == ExpandCollapseState.Expanded:
                state |= State.Expanded
            elif temp == ExpandCollapseState.PartiallyExpanded:
                state |= State.PartiallyExpanded
            else:
                state |= State.Leaf
        
        if self.selected:
            state |= State.Selected
        
        if self.focusable:
            state |= State.KeyBoardFocusable
        
        if self.focused:
            state |= State.KeyBoardFocused
            
        if self.is_topmost:
            state |= State.TopMost
        
        if self.is_modal:
            state |= State.Modal
        
        return state
    
    @state.setter
    def state(self, value):
        temp = value & WindowVisualState.Maximized                
        if temp > 0:
            self.__pattern_set('window', 'visualstate', temp)
        else:
            temp = value & WindowVisualState.Minimized
            if temp > 0:
                self.__pattern_set('window', 'visualstate', temp)
            else:
                temp = value & WindowVisualState.Normal
                if temp > 0:
                    self.__pattern_set('window', 'visualstate', temp)
    
    @property
    def selected(self):
        return bool(self.__pattern_get('selectionitem', 'selected'))
    
    @property
    def is_topmost(self):
        return bool(self.__pattern_get('window', 'topmost'))
    
    @property
    def is_modal(self):
        return bool(self.__pattern_get('window', 'modal'))
    
    @property
    def can_max(self):
        return bool(self.__pattern_get('window', 'canmax'))
    
    @property
    def can_min(self):
        return bool(self.__pattern_get('window', 'canmin'))
    
    def close(self):
        self.__pattern_call('window', 'close')    
    
    @property
    def movable(self):
        return bool(self.__pattern_get('transform', 'canmove'))
    
    @property
    def sizable(self):
        return bool(self.__pattern_get('transform', 'canresize'))      
    
    @property
    def currentvalue(self):        
        return self.__pattern_get('rangevalue', 'value')
    
    @property
    def maxvalue(self):
        return self.__pattern_get('rangevalue', 'max')        
    
    @property
    def minvalue(self):
        return self.__pattern_get('rangevalue', 'min')
    
    @property
    def smallchange(self):
        return self.__pattern_get('rangevalue', 'smallchange')
            
    @property
    def largechange(self):
        return self.__pattern_get('rangevalue', 'largechange')  
    
    @property
    def value(self):
        return self.__pattern_get('value', 'value')
    
    @property
    def readonly(self):
        return bool(self.__pattern_get('value', 'readonly'))
    
    @property
    def text(self):
        txt = self.value
        if txt is None:
            txt = self.name
        return txt
    
    @text.setter
    def text(self, value):
        if self.readonly != True: 
            if self._host.value != None:
                self.__pattern_set('value', 'value', value)
        else:
            self.sendkeys(value)    
   
    def toggle(self):
        self.__pattern_call('toggle', 'toggle')
    
    def expand(self):
        self.__pattern_call('expcol', 'expand')
    
    def collapse(self):
        self.__pattern_call('expcol', 'collapse')
        
    def select(self):
        self.__pattern_call('selectionitem', 'select')
    
    def add_to_selection(self):
        self.__pattern_call('selectionitem', 'add2selection')
    
    def remove_from_selection(self):
        self.__pattern_call('selectionitem', 'remove_from_selection')
    
    @property
    def selection(self):
        return [Element(x) for x in self.__pattern_get('selection', 'selection')]
    
    def scroll_into_view(self):
        self.__pattern_call('scrollitem', 'ScrollIntoView')
    
    
    
    

