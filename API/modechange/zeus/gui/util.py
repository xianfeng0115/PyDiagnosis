

def decode(string):
    for codec in ['gb18030', 'gb2312', 'utf-8']:
        try:
            string = string.decode(codec)
            break
        except:
            pass
    return string

class Condition(object):
    def __init__(self, scope = 1, index = 0, timeout = 3, delay = 0, **condition):
        self.delay = delay        
        self.scope = scope #QueryScope.Descendants
        self.index = index
        self.timeout = timeout
        self.condition = condition
    
    def __repr__(self):
        return '[scope:%d, index:%d, timeout:%d, delay:%d, condition:%s]' % (
                                                                           self.scope,
                                                                           self.index,
                                                                           self.timeout,
                                                                           self.delay,
                                                                           repr(self.condition)
                                                                           )
    

class QueryId(object):        
    def __init__(self, start = None, totaltime = -1, criteria = None, **condition):
        self.start = start
        self.totaltime = totaltime
        self.criteria = []
        self._create_criteria(criteria)
        if len(condition)>0:
            self.criteria.append(Condition(**condition))
    
    def _create_criteria(self, criteria):
        if criteria is not None:
            for con in criteria:
                self.criteria.append(Condition(**con))
        
    
    def __repr__(self):
        return '<totaltime:%d, criteria:%s>' % (
                                                 self.totaltime,
                                                 repr(self.criteria)
                                                )

class QueryScope(object):
    Ancestors = 0
    Descendants = 1
    Children = 2
    Siblings = 3    

class Role:
    Element     = 'element'
    Window      = 'window'
    Button      = 'button'
    Edit        = 'edit'
    Text        = 'text'
    ProcessBar  = 'processbar'
    Pane        = 'pane'
    List        = 'list'
    ListItem    = 'listitem'
    Menu        = 'menu'
    MenuItem    = 'menuitem'
    TitleBar    = 'titlebar'
    Tooltip     = 'tooltip'
    ToolBar     = 'toolbar'
    CheckBox    = 'checkbox'
    ComboBox    = 'combobox'
    Grid        = 'grid'
    GridItem    = 'griditem'
    Group       = 'group'
    Hyperlink   = 'hyperlink'
    Image       = 'image'
    MenuBar     = 'menubar'
    RadioButton = 'radiobutton'
    ScrollBar   = 'scrollbar'
    Slider      = 'slider'
    Spinner     = 'spinner'
    SplitButton = 'splitbutton'
    StatusBar   = 'statusbar'
    Tab         = 'tab'
    TabItem     = 'tabitem'
    Table       = 'table'
    Thumb       = 'thumb'
    Tree        = 'tree'
    TreeItem    = 'treeitem'
    

#class DockPosition(object):
#    Top = 'Top'
#    Left = 'Left'
#    Bottom = 'Bottom'
#    Right = 'Right'
#    Fill = 'Fill'
#    Null = 'Null'

class MouseAction:
    Click = 0
    DoubleClick = 1
    Move = 2

class MouseButton:
    Left = 0
    Right = 1
    Middle = 2

class State:
    KeyBoardFocused     = 0b00000000000000000000001
    KeyBoardFocusable   = 0b00000000000000000000010
    Expanded            = 0b00000000000000000000100
    Collapsed           = 0b00000000000000000001000
    ToggledOn           = 0b00000000000000000010000
    ToggledOff            = 0b00000000000000000100000
    IndeterminateToggled = 0b00000000000000001000000
    Selected            = 0b00000000000000010000000
    Password            = 0b00000000000000100000000
    Movable             = 0b00000000000001000000000
    Sizable               = 0b00000000000010000000000
    Modal               = 0b00000000000100000000000
    Maximized           = 0b00000000001000000000000
    Minimized           = 0b00000000010000000000000
    Normal              = 0b00000000100000000000000
    TopMost             = 0b00000001000000000000000
    PartiallyExpanded   = 0b00000010000000000000000
    Leaf                = 0b00000100000000000000000
    

class Property:    
    Name        = 'name'
    ClassName   = 'classname'
    Role        = 'role'
    Location    = 'location'
    Id          = 'id'
    RuntimeId   = 'runtimeid'
    ProcessId   = 'processid'
    State       = 'state'
    Enabled     = 'enabled'
    Offscreen   = 'offscreen'
    Available   = 'available'        
    ReadOnly    = 'readonly'
    Text        = 'text'        
    Value       = 'value'
    Maximum     = 'maximum'
    Minimum     = 'minimum'
    LargeChange = 'largechange'
    SmallChange = 'smallchange'
        

class Method:    
    Click       = 'click'
    DoubleClick = 'doubleclick'
    SetFocus    = 'setfocus'
    MouseMove   = 'mousemove'
    SendKeys    = 'sendkeys'
    Close       = 'close'
    Toggle      = 'toggle'
    Expand      = 'expand'
    Collapse    = 'collapse'
    Select      = 'select'
    
    
class SpecialChar:
    Return     = 'RETURN'
    Menu       = 'MENU'
    Capital    = 'CAPITAL'
    Escape     = 'ESCAPE'
    Space      = 'SPACE'
    Next       = 'NEXT'
    End        = 'END'
    Home       = 'HOME'
    Left       = 'LEFT'
    Up         = 'UP'
    Right      = 'RIGHT'
    Down       = 'DOWN'
    Snapshot   = 'SNAPSHOT'
    Insert     = 'INSERT'
    Delete     = 'DELETE'
    Control    = 'CONTROL'
    