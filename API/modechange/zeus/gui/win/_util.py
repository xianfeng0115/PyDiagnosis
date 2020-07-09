
#from _role import Role
import comtypes.client, _uia
from zeus.gui.util import Role
from ctypes import POINTER, byref
from _ctypes import COMError

UIA_Interface = comtypes.client.CreateObject(_uia.CUIAutomation)
UIA_TrueCondition = UIA_Interface.CreateTrueCondition()
UIA_FalseCondition = UIA_Interface.CreateFalseCondition()
UIA_CtrlViewCondition = UIA_Interface.ControlViewCondition
UIA_CtrlViewWalker = UIA_Interface.ControlViewWalker


def get_root():
    found = UIA_Interface.GetRootElement()
    if str(found).find('ptr=0x0') > 0: 
        return None
    else:
        return UIAElement(found)

def get_parent(host):        
    found = UIA_CtrlViewWalker.GetParentElement(host._raw)
    if str(found).find('ptr=0x0') > 0:
        return None
    else:
        return UIAElement(found)
        
def get_firstchild(host):
    found = UIA_CtrlViewWalker.GetFirstChildElement(host._raw)
    if str(found).find('ptr=0x0') > 0:
        return None
    else:
        return UIAElement(found)
    
def get_lastchild(host):
    found = UIA_CtrlViewWalker.GetLastChildElement(host._raw)
    if str(found).find('ptr=0x0') > 0:
        return None
    else:
        return UIAElement(found)
    
def get_nextsibling(host):
    found = UIA_CtrlViewWalker.GetNextSiblingElement(host._raw)
    if str(found).find('ptr=0x0') > 0:
        return None
    else:
        return UIAElement(found)
    
def get_prevsibling(host):
    found = UIA_CtrlViewWalker.GetPreviousSiblingElement(host._raw)
    if str(found).find('ptr=0x0') > 0:
        return None
    else:
        return UIAElement(found)
    
def get_children(host):
    elements = host._raw.FindAll(_uia.TreeScope_Children,UIA_TrueCondition)
    if str(elements).find('ptr=0x0') > 0:
        return None
    return [UIAElement(elements.GetElement(i)) for i in xrange(elements.Length)]





class RoleMap(object):
    _map = {
                    _uia.UIA_ButtonControlTypeId        : Role.Button,
                    _uia.UIA_CheckBoxControlTypeId      : Role.CheckBox,
                    _uia.UIA_ComboBoxControlTypeId      : Role.ComboBox,
                    _uia.UIA_EditControlTypeId          : Role.Edit,
                    _uia.UIA_DataGridControlTypeId      : Role.Grid,
                    _uia.UIA_DataItemControlTypeId      : Role.GridItem,
                    _uia.UIA_GroupControlTypeId         : Role.Group,
                    _uia.UIA_HyperlinkControlTypeId     : Role.Hyperlink ,
                    _uia.UIA_ImageControlTypeId         : Role.Image,
                    _uia.UIA_ListControlTypeId          : Role.List,
                    _uia.UIA_ListItemControlTypeId      : Role.ListItem ,
                    _uia.UIA_MenuControlTypeId          : Role.Menu,
                    _uia.UIA_MenuItemControlTypeId      : Role.MenuItem,
                    _uia.UIA_MenuBarControlTypeId       : Role.MenuBar,
                    _uia.UIA_PaneControlTypeId          : Role.Pane,
                    _uia.UIA_ProgressBarControlTypeId   : Role.ProcessBar,
                    _uia.UIA_RadioButtonControlTypeId   : Role.RadioButton,
                    _uia.UIA_TextControlTypeId          : Role.Text,
                    _uia.UIA_ScrollBarControlTypeId     : Role.ScrollBar,
                    _uia.UIA_SliderControlTypeId        : Role.Slider,
                    _uia.UIA_SpinnerControlTypeId       : Role.Spinner,
                    _uia.UIA_SplitButtonControlTypeId   : Role.SplitButton,
                    _uia.UIA_StatusBarControlTypeId     : Role.StatusBar,
                    _uia.UIA_ToolTipControlTypeId       : Role.Tooltip,
                    _uia.UIA_ToolBarControlTypeId       : Role.ToolBar,
                    _uia.UIA_TitleBarControlTypeId      : Role.TitleBar,
                    _uia.UIA_TabControlTypeId           : Role.Tab,
                    _uia.UIA_TabItemControlTypeId       : Role.TabItem,
                    _uia.UIA_TableControlTypeId         : Role.Table,
                    _uia.UIA_ThumbControlTypeId         : Role.Thumb,
                    _uia.UIA_TreeControlTypeId          : Role.Tree,
                    _uia.UIA_TreeItemControlTypeId      : Role.TreeItem,                       
                    _uia.UIA_WindowControlTypeId        : Role.Window,        
                   }    
    
    @staticmethod
    def role(host):
        return RoleMap._map.get(host.com_invoke('CurrentControlType'), 'undefined')  

class ComInvoke(object):
    def __init__(self, raw):
        #if raw is None: raise Exception('UIA element or pattern cannot be none.')
        self._raw = raw
    
    def com_invoke(self, name, *args, **kargs):
        if self._raw == None: return None
        try:
            if not hasattr(self._raw, name) : return None
            attr = getattr(self._raw, name)
            prototype = getattr(self._raw.__class__,name)
            if prototype.__class__.__name__ == 'property':
                return attr
            else:
                return attr(*args, **kargs)
        except COMError:
            return None

class UIAElementArray(ComInvoke):
    def __init__(self, array):
        ComInvoke.__init__(self, array)
        
    @property
    def length(self):
        return self.com_invoke('Length')
    
    def getelement(self, index):
        return UIAElement(self.com_invoke('GetElement', index))

class CommonPattern(ComInvoke):
    def __init__(self, uia):
        ComInvoke.__init__(self, uia)
    
    

class UIAElement(ComInvoke):
    
    ptnclses = {}
    
    def __init__(self, raw):
        ComInvoke.__init__(self, raw)
        self._patterns = {}
    
    def get_hwnd(self):
        return self.com_invoke('CurrentNativeWindowHandle')
    
    def get_name(self):
        return self.com_invoke('CurrentName')
    
    def get_id(self):
        return self.com_invoke('CurrentAutomationId')
    
    def get_rtid(self):
        return self.com_invoke('GetRuntimeId')
    
    def get_classname(self):
        return self.com_invoke('CurrentClassName')
    
    def get_pid(self):
        return self.com_invoke('CurrentProcessId')
    
    def get_location(self):
        loc = self.com_invoke('CurrentBoundingRectangle')
        return (loc.left,loc.top, loc.right, loc.bottom)
        
    def get_visible(self):
        return not self.com_invoke('CurrentIsOffscreen')
    
    def get_role(self):
        return RoleMap.role(self)
    
    def get_enabled(self):
        return bool(self.com_invoke('CurrentIsEnabled'))
    
    def get_focused(self):
        return bool(self.com_invoke('CurrentHasKeyboardFocus'))
    
    def get_focusable(self):
        return bool(self.com_invoke('CurrentIsKeyboardFocusable'))
    
    def get_password(self):
        return bool(self.com_invoke('CurrentIsPassword'))
    
    def setfocus(self):
        self.com_invoke('SetFocus')  
    
    def _has_pattern(self, vid):
        return bool(self.com_invoke('GetCurrentPropertyValue' , vid))
    
    def _pattern_from_cls(self, ptncls):
        pa = ptncls.klass
        return ptncls(POINTER(pa)(self.com_invoke('GetCurrentPatternAs',pa._pid_, byref(pa._iid_))))
    
    def _pattern(self, name):
        ptncls = self.ptnclses[name]
        if self._has_pattern(ptncls.klass._vid_):
            if not self._patterns.has_key(name):                
                self._patterns[name] = self._pattern_from_cls(ptncls)
        return self._patterns.get(name, None)
    
    @property
    def window(self):
        return self._pattern('window')    
    @property
    def value(self):
        return self._pattern('value')    
    @property
    def invoke(self):
        return self._pattern('invoke')    
    @property
    def expcol(self):
        return self._pattern('expcol')    
    @property
    def dock(self):
        return self._pattern('dock')    
    @property
    def griditem(self):
        return self._pattern('griditem')
    @property
    def grid(self):
        return self._pattern('grid')
    @property
    def rangevalue(self):
        return self._pattern('rangevalue')
    @property
    def scrollitem(self):
        return self._pattern('scrollitem')
    @property
    def scroll(self):
        return self._pattern('scroll')
    @property
    def selection(self):
        return self._pattern('selection')
    @property
    def selectionitem(self):
        return self._pattern('selectionitem')
    @property
    def table(self):
        return self._pattern('table')
    @property
    def tableitem(self):
        return self._pattern('tableitem')
    @property
    def text(self):
        return self._pattern('text')
    @property
    def toggle(self):
        return self._pattern('toggle')
    @property
    def transform(self):
        return self._pattern('transform')
    

class Pattern(ComInvoke):
    klass = None
    
    def __init__(self, pattern):            
        ComInvoke.__init__(self, pattern)


class WindowPattern(Pattern):
    klass = _uia.IUIAutomationWindowPattern    
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
        
    def get_modal(self):
        return bool(self.com_invoke('CurrentIsModal'))
    
    def get_topmost(self):
        return bool(self.com_invoke('CurrentIsTopmost'))
    
    def close(self):
        self.com_invoke('Close')
    
    def get_canmax(self):
        return bool(self.com_invoke('CurrentCanMaximize'))
    
    def get_canmin(self):
        return bool(self.com_invoke('CurrentCanMinimize'))
    
    def get_visualstate(self):
        return self.com_invoke('CurrentWindowVisualState')
    
    def set_visualstate(self, state):
        return self.com_invoke('SetWindowVisualState', state)

class ValuePattern(Pattern):
    klass = _uia.IUIAutomationValuePattern
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def get_value(self):
        return self.com_invoke('CurrentValue')
    
    def set_value(self, value):
        self.com_invoke('SetValue', value)
    
    def get_readonly(self):
        return self.com_invoke('CurrentIsReadOnly')
    
class InvokePattern(Pattern):
    klass = _uia.IUIAutomationInvokePattern
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def invoke(self):
        self.com_invoke('Invoke')
    

class ExpandCollapsePattern(Pattern):
    klass = _uia.IUIAutomationExpandCollapsePattern    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def collapse(self):
        self.com_invoke('Collapse')
    
    def expand(self):
        self.com_invoke('Expand')
    
    def get_state(self):
        return self.com_invoke('CurrentExpandCollapseState')
        

class DockPattern(Pattern):
    klass = _uia.IUIAutomationDockPattern    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def get_dockposition(self):
        return self.com_invoke('CurrentDockPosition')
    
    def set_dockposition(self, pos):
        self.com_invoke('SetDockPosition', pos)

class GridItemPattern(Pattern):
    klass = _uia.IUIAutomationGridItemPattern
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def get_row(self):
        return self.com_invoke('CurrentRow')
    
    def get_rowspan(self):
        return self.com_invoke('CurrentRowSpan')
    
    def get_column(self):
        return self.com_invoke('CurrentColumn')
    
    def get_columnspan(self):
        return self.com_invoke('CurrentColumnSpan')

class GridPattern(Pattern):
    klass = _uia.IUIAutomationGridPattern
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def getitem(self, row, column):
        return self.com_invoke('GetItem', row, column)        
    
    def get_rowcount(self):
        return self.com_invoke('CurrentRowCount')    
    
    def get_columncount(self):
        return self.com_invoke('CurrentColumnCount')    


class RangeValuePattern(Pattern):
    klass = _uia.IUIAutomationRangeValuePattern
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def get_value(self):
        return self.com_invoke('CurrentValue')
    
    def set_value(self, value):
        self.com_invoke('SetValue', value)
    
    def get_readonly(self):
        return self.com_invoke('CurrentIsReadOnly')
    
    def get_max(self):
        return self.com_invoke('CurrentMaximum')
    
    def get_min(self):
        return self.com_invoke('CurrentMinimum')
    
    def get_largechange(self):
        return self.com_invoke('CurrentLargeChange')
    
    def get_smallchange(self):
        return self.com_invoke('CurrentSmallChange')
        
class ScrollPattern(Pattern):
    klass = _uia.IUIAutomationScrollPattern
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def scroll_by_amount(self, hor, ver):
        self.com_invoke('Scroll', hor, ver)
    
    def scroll_by_percent(self, hor, ver):
        self.com_invoke('SetScrollPercent', hor, ver)
        
    def get_hor_percent(self):
        return self.com_invoke('CurrentHorizontalScrollPercent')
    
    def get_ver_percent(self):
        return self.com_invoke('CurrentVerticalScrollPercent')
    
    def get_hor_size(self):
        return self.com_invoke('CurrentHorizontalViewSize')
    
    def get_ver_size(self):
        return self.com_invoke('CurrentVerticalViewSize')
    
    def get_hor_scrollable(self):
        return self.com_invoke('CurrentHorizontallyScrollable')
    
    def get_ver_scrollable(self):
        return self.com_invoke('CurrentVerticallyScrollable')

class ScrollItemPattern(Pattern):
    klass = _uia.IUIAutomationScrollItemPattern
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def scroll_into_view(self):
        self.com_invoke('ScrollIntoView')

class SelectionPattern(Pattern):
    klass = _uia.IUIAutomationSelectionPattern
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def get_selection_mutiple(self):
        return bool(self.com_invoke('CurrentCanSelectMultiple'))
    
    def get_selection_required(self):
        return bool(self.com_invoke('CurrentIsSelectionRequired'))
    
    def get_selection(self):
        return UIAElementArray(self.com_invoke('GetCurrentSelection'))

class SelectionItemPattern(Pattern):
    klass = _uia.IUIAutomationSelectionItemPattern
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
        
    def select(self):
        self.com_invoke('Select')
    
    def add2selection(self):
        self.com_invoke('AddToSelection')
    
    def remove_from_selection(self):
        self.com_invoke('RemoveFromSelection')
    
    def get_selected(self):
        return bool(self.com_invoke('CurrentIsSelected'))
    
    def get_container(self):
        return UIAElement(self.com_invoke('CurrentSelectionContainer'))
    

class TablePattern(Pattern):
    klass = _uia.IUIAutomationTablePattern
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def get_rowheaders(self):
        return UIAElementArray(self.com_invoke('GetCurrentRowHeaders'))
    
    def get_columnheaders(self):
        return UIAElementArray(self.com_invoke('GetCurrentColumnHeaders'))
    
class TableItemPattern(Pattern):
    klass = _uia.IUIAutomationTableItemPattern
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
        
    def get_rowheaderitems(self):
        return UIAElementArray(self.com_invoke('GetCurrentRowHeaderItems'))
    
    def get_columnheaderitems(self):
        return UIAElementArray(self.com_invoke('GetCurrentColumnHeaderItems'))
    
class TextPattern(Pattern):
    '''Need to be implemented.'''
    klass = _uia.IUIAutomationTextPattern
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
        

class TogglePattern(Pattern):    
    klass = _uia.IUIAutomationTogglePattern
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def toggle(self):
        self.com_invoke('Toggle')
    
    def get_togglestate(self):
        return self.com_invoke('CurrentToggleState')

class TransformPattern(Pattern):    
    klass = _uia.IUIAutomationTransformPattern
    
    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
    
    def move(self, x, y):
        self.com_invoke('Move', x, y)
    
    def resize(self, width, height):
        self.com_invoke('Resize', width, height)
        
    def Rotate(self, degrees):
        self.com_invoke('Rotate', degrees)
    
    def get_canmove(self):
        return bool(self.com_invoke('CurrentCanMove'))
    
    def get_canresize(self):
        return bool(self.com_invoke('CurrentCanResize'))
        
    def get_canrotate(self):
        return bool(self.com_invoke('CurrentCanRotate'))

UIAElement.ptnclses.update(
                           {
                            'window':WindowPattern,
                            'value':ValuePattern,
                            'invoke':InvokePattern,
                            'expcol':ExpandCollapsePattern,
                            'dock':DockPattern,
                            'griditem':GridItemPattern,
                            'grid':GridPattern,
                            'rangevalue':RangeValuePattern,
                            'scroll':ScrollPattern,
                            'scrollitem':ScrollItemPattern,
                            'selection':SelectionPattern,
                            'selectionitem':SelectionItemPattern,
                            'table':TablePattern,
                            'tableitem':TableItemPattern,
                            'text':TextPattern,
                            'toggle':TogglePattern,
                            'transform':TransformPattern,
                            
                            }
                           )
     
