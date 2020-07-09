# -*- coding: mbcs -*-
typelib_path = 'UIAutomationCore.dll'
_lcid = 0 # change this if required
from ctypes import *
from comtypes import CoClass, IUnknown, GUID, HRESULT, BSTR, helpstring, COMMETHOD, dispid, _check_version
from comtypes.automation import _midlSAFEARRAY, VARIANT, IDispatch

WSTRING = c_wchar_p
from ctypes.wintypes import tagRECT
from ctypes.wintypes import tagPOINT


UIA_GridItemColumnPropertyId = 30065 # Constant c_int
UIA_ValuePatternId = 10002 # Constant c_int
UIA_GridItemColumnSpanPropertyId = 30067 # Constant c_int
UIA_AriaPropertiesPropertyId = 30102 # Constant c_int
UIA_DockPatternId = 10011 # Constant c_int
UIA_DockDockPositionPropertyId = 30069 # Constant c_int
UIA_TabItemControlTypeId = 50019 # Constant c_int
UIA_MultipleViewCurrentViewPropertyId = 30071 # Constant c_int
UIA_MultipleViewSupportedViewsPropertyId = 30072 # Constant c_int
UIA_AsyncContentLoadedEventId = 20006 # Constant c_int
UIA_AutomationPropertyChangedEventId = 20004 # Constant c_int
UIA_IsDataValidForFormPropertyId = 30103 # Constant c_int
UIA_DescribedByPropertyId = 30105 # Constant c_int
UIA_ToolTipOpenedEventId = 20000 # Constant c_int
UIA_ScrollItemPatternId = 10017 # Constant c_int
UIA_TablePatternId = 10012 # Constant c_int
UIA_SelectionPatternId = 10001 # Constant c_int
UIA_ItemContainerPatternId = 10019 # Constant c_int
UIA_TransformPatternId = 10016 # Constant c_int
UIA_VirtualizedItemPatternId = 10020 # Constant c_int
UIA_ItemStatusPropertyId = 30026 # Constant c_int
UIA_IsDockPatternAvailablePropertyId = 30027 # Constant c_int
UIA_IsExpandCollapsePatternAvailablePropertyId = 30028 # Constant c_int
UIA_IsGridItemPatternAvailablePropertyId = 30029 # Constant c_int
UIA_IsGridPatternAvailablePropertyId = 30030 # Constant c_int
UIA_IsInvokePatternAvailablePropertyId = 30031 # Constant c_int
UIA_TransformCanRotatePropertyId = 30089 # Constant c_int
UIA_TransformCanMovePropertyId = 30087 # Constant c_int
UIA_IsRangeValuePatternAvailablePropertyId = 30033 # Constant c_int
UIA_IsScrollPatternAvailablePropertyId = 30034 # Constant c_int
UIA_IsScrollItemPatternAvailablePropertyId = 30035 # Constant c_int
UIA_ExpandCollapseExpandCollapseStatePropertyId = 30070 # Constant c_int
UIA_IsSelectionPatternAvailablePropertyId = 30037 # Constant c_int
UIA_IsTablePatternAvailablePropertyId = 30038 # Constant c_int
UIA_IsTableItemPatternAvailablePropertyId = 30039 # Constant c_int
UIA_IsTextPatternAvailablePropertyId = 30040 # Constant c_int
UIA_IsTogglePatternAvailablePropertyId = 30041 # Constant c_int
UIA_IsTransformPatternAvailablePropertyId = 30042 # Constant c_int
UIA_OverlineStyleAttributeId = 40024 # Constant c_int
UIA_IsValuePatternAvailablePropertyId = 30043 # Constant c_int
UIA_IsWindowPatternAvailablePropertyId = 30044 # Constant c_int
UIA_ValueValuePropertyId = 30045 # Constant c_int
UIA_ValueIsReadOnlyPropertyId = 30046 # Constant c_int
UIA_MarginLeadingAttributeId = 40019 # Constant c_int
UIA_MenuOpenedEventId = 20003 # Constant c_int
UIA_IsItemContainerPatternAvailablePropertyId = 30108 # Constant c_int
UIA_IsVirtualizedItemPatternAvailablePropertyId = 30109 # Constant c_int
UIA_IsMultipleViewPatternAvailablePropertyId = 30032 # Constant c_int


class IUIAutomationProxyFactoryEntry(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{D50E472E-B64B-490C-BCA1-D30696F9F289}')
    _idlflags_ = []
class IUIAutomationProxyFactory(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{85B94ECD-849D-42B6-B94D-D6DB23FDF5A4}')
    _idlflags_ = []
IUIAutomationProxyFactoryEntry._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ProxyFactory',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationProxyFactory)), 'factory' )),
    COMMETHOD(['propget'], HRESULT, 'ClassName',
              ( ['retval', 'out'], POINTER(BSTR), 'ClassName' )),
    COMMETHOD(['propget'], HRESULT, 'ImageName',
              ( ['retval', 'out'], POINTER(BSTR), 'ImageName' )),
    COMMETHOD(['propget'], HRESULT, 'AllowSubstringMatch',
              ( ['retval', 'out'], POINTER(c_int), 'AllowSubstringMatch' )),
    COMMETHOD(['propget'], HRESULT, 'CanCheckBaseClass',
              ( ['retval', 'out'], POINTER(c_int), 'CanCheckBaseClass' )),
    COMMETHOD(['propget'], HRESULT, 'NeedsAdviseEvents',
              ( ['retval', 'out'], POINTER(c_int), 'adviseEvents' )),
    COMMETHOD(['propput'], HRESULT, 'ClassName',
              ( ['in'], WSTRING, 'ClassName' )),
    COMMETHOD(['propput'], HRESULT, 'ImageName',
              ( ['in'], WSTRING, 'ImageName' )),
    COMMETHOD(['propput'], HRESULT, 'AllowSubstringMatch',
              ( ['in'], c_int, 'AllowSubstringMatch' )),
    COMMETHOD(['propput'], HRESULT, 'CanCheckBaseClass',
              ( ['in'], c_int, 'CanCheckBaseClass' )),
    COMMETHOD(['propput'], HRESULT, 'NeedsAdviseEvents',
              ( ['in'], c_int, 'adviseEvents' )),
    COMMETHOD([], HRESULT, 'SetWinEventsForAutomationEvent',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], _midlSAFEARRAY(c_uint), 'winEvents' )),
    COMMETHOD([], HRESULT, 'GetWinEventsForAutomationEvent',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(c_uint)), 'winEvents' )),
]


UIA_StructureChangedEventId = 20002 # Constant c_int
UIA_AutomationFocusChangedEventId = 20005 # Constant c_int
UIA_BoundingRectanglePropertyId = 30001 # Constant c_int
UIA_MenuClosedEventId = 20007 # Constant c_int
UIA_LayoutInvalidatedEventId = 20008 # Constant c_int
UIA_Invoke_InvokedEventId = 20009 # Constant c_int
UIA_SelectionItem_ElementAddedToSelectionEventId = 20010 # Constant c_int
UIA_SelectionItem_ElementRemovedFromSelectionEventId = 20011 # Constant c_int
UIA_SelectionItem_ElementSelectedEventId = 20012 # Constant c_int
class IUIAutomationDockPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{FDE5EF97-1464-48F6-90BF-43D0948E86EC}')
    _idlflags_ = []
    _pid_ = UIA_DockPatternId
    _vid_ = UIA_IsDockPatternAvailablePropertyId

# values for enumeration 'DockPosition'
DockPosition_Top = 0
DockPosition_Left = 1
DockPosition_Bottom = 2
DockPosition_Right = 3
DockPosition_Fill = 4
DockPosition_None = 5
DockPosition = c_int # enum
IUIAutomationDockPattern._methods_ = [
    COMMETHOD([], HRESULT, 'SetDockPosition',
              ( ['in'], DockPosition, 'dockPos' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDockPosition',
              ( ['retval', 'out'], POINTER(DockPosition), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDockPosition',
              ( ['retval', 'out'], POINTER(DockPosition), 'retVal' )),
]


UIA_Text_TextSelectionChangedEventId = 20014 # Constant c_int
UIA_Text_TextChangedEventId = 20015 # Constant c_int
UIA_Window_WindowOpenedEventId = 20016 # Constant c_int
UIA_GridItemContainingGridPropertyId = 30068 # Constant c_int
UIA_Window_WindowClosedEventId = 20017 # Constant c_int
UIA_MenuModeStartEventId = 20018 # Constant c_int
UIA_FlowsToPropertyId = 30106 # Constant c_int
UIA_InputReachedTargetEventId = 20020 # Constant c_int
UIA_InputReachedOtherElementEventId = 20021 # Constant c_int
UIA_InputDiscardedEventId = 20022 # Constant c_int
UIA_RuntimeIdPropertyId = 30000 # Constant c_int
UIA_ProcessIdPropertyId = 30002 # Constant c_int
class IRawElementProviderSimple(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{D6DD68D1-86FD-4332-8666-9ABEDEA2D24C}')
    _idlflags_ = []
IUIAutomationProxyFactory._methods_ = [
    COMMETHOD([], HRESULT, 'CreateProvider',
              ( ['in'], c_void_p, 'hwnd' ),
              ( ['in'], c_int, 'idObject' ),
              ( ['in'], c_int, 'idChild' ),
              ( ['retval', 'out'], POINTER(POINTER(IRawElementProviderSimple)), 'provider' )),
    COMMETHOD(['propget'], HRESULT, 'ProxyFactoryId',
              ( ['retval', 'out'], POINTER(BSTR), 'factoryId' )),
]

UIA_ControlTypePropertyId = 30003 # Constant c_int
UIA_BackgroundColorAttributeId = 40001 # Constant c_int
UIA_LocalizedControlTypePropertyId = 30004 # Constant c_int
UIA_NamePropertyId = 30005 # Constant c_int
UIA_AcceleratorKeyPropertyId = 30006 # Constant c_int
UIA_AccessKeyPropertyId = 30007 # Constant c_int
class IUIAutomationVirtualizedItemPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{6BA3D7A6-04CF-4F11-8793-A8D1CDE9969F}')
    _idlflags_ = []
    _pid_ = UIA_VirtualizedItemPatternId
    _vid_ = UIA_IsVirtualizedItemPatternAvailablePropertyId
IUIAutomationVirtualizedItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Realize'),
]


UIA_IsKeyboardFocusablePropertyId = 30009 # Constant c_int
UIA_IsEnabledPropertyId = 30010 # Constant c_int
UIA_AutomationIdPropertyId = 30011 # Constant c_int
UIA_GridItemRowSpanPropertyId = 30066 # Constant c_int
UIA_SeparatorControlTypeId = 50038 # Constant c_int
UIA_HelpTextPropertyId = 30013 # Constant c_int
UIA_ClickablePointPropertyId = 30014 # Constant c_int
UIA_LegacyIAccessibleNamePropertyId = 30092 # Constant c_int
UIA_CulturePropertyId = 30015 # Constant c_int
UIA_EditControlTypeId = 50004 # Constant c_int
UIA_IsControlElementPropertyId = 30016 # Constant c_int
UIA_IsContentElementPropertyId = 30017 # Constant c_int
UIA_SelectionItemSelectionContainerPropertyId = 30080 # Constant c_int
UIA_LabeledByPropertyId = 30018 # Constant c_int
UIA_IsPasswordPropertyId = 30019 # Constant c_int
UIA_SynchronizedInputPatternId = 10021 # Constant c_int
UIA_NativeWindowHandlePropertyId = 30020 # Constant c_int
UIA_ItemTypePropertyId = 30021 # Constant c_int

# values for enumeration 'ProviderOptions'
ProviderOptions_ClientSideProvider = 1
ProviderOptions_ServerSideProvider = 2
ProviderOptions_NonClientAreaProvider = 4
ProviderOptions_OverrideProvider = 8
ProviderOptions_ProviderOwnsSetFocus = 16
ProviderOptions_UseComThreading = 32
ProviderOptions = c_int # enum
IRawElementProviderSimple._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ProviderOptions',
              ( ['retval', 'out'], POINTER(ProviderOptions), 'pRetVal' )),
    COMMETHOD([], HRESULT, 'GetPatternProvider',
              ( ['in'], c_int, 'patternId' ),
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'pRetVal' )),
    COMMETHOD([], HRESULT, 'GetPropertyValue',
              ( ['in'], c_int, 'propertyId' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pRetVal' )),
    COMMETHOD(['propget'], HRESULT, 'HostRawElementProvider',
              ( ['retval', 'out'], POINTER(POINTER(IRawElementProviderSimple)), 'pRetVal' )),
]


UIA_OrientationPropertyId = 30023 # Constant c_int
UIA_FrameworkIdPropertyId = 30024 # Constant c_int
UIA_IsRequiredForFormPropertyId = 30025 # Constant c_int
class IUIAutomationLegacyIAccessiblePattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{828055AD-355B-4435-86D5-3B51C14A9B1B}')
    _idlflags_ = []
class IUIAutomationElementArray(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{14314595-B4BC-4055-95F2-58F2E42C9855}')
    _idlflags_ = []
class IAccessible(IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{618736E0-3C3D-11CF-810C-00AA00389B71}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
IUIAutomationLegacyIAccessiblePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Select',
              ( [], c_int, 'flagsSelect' )),
    COMMETHOD([], HRESULT, 'DoDefaultAction'),
    COMMETHOD([], HRESULT, 'SetValue',
              ( [], WSTRING, 'szValue' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentChildId',
              ( ['retval', 'out'], POINTER(c_int), 'pRetVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentName',
              ( ['retval', 'out'], POINTER(BSTR), 'pszName' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentValue',
              ( ['retval', 'out'], POINTER(BSTR), 'pszValue' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDescription',
              ( ['retval', 'out'], POINTER(BSTR), 'pszDescription' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRole',
              ( ['retval', 'out'], POINTER(c_ulong), 'pdwRole' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentState',
              ( ['retval', 'out'], POINTER(c_ulong), 'pdwState' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHelp',
              ( ['retval', 'out'], POINTER(BSTR), 'pszHelp' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentKeyboardShortcut',
              ( ['retval', 'out'], POINTER(BSTR), 'pszKeyboardShortcut' )),
    COMMETHOD([], HRESULT, 'GetCurrentSelection',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'pvarSelectedChildren' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDefaultAction',
              ( ['retval', 'out'], POINTER(BSTR), 'pszDefaultAction' )),
    COMMETHOD(['propget'], HRESULT, 'CachedChildId',
              ( ['retval', 'out'], POINTER(c_int), 'pRetVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedName',
              ( ['retval', 'out'], POINTER(BSTR), 'pszName' )),
    COMMETHOD(['propget'], HRESULT, 'CachedValue',
              ( ['retval', 'out'], POINTER(BSTR), 'pszValue' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDescription',
              ( ['retval', 'out'], POINTER(BSTR), 'pszDescription' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRole',
              ( ['retval', 'out'], POINTER(c_ulong), 'pdwRole' )),
    COMMETHOD(['propget'], HRESULT, 'CachedState',
              ( ['retval', 'out'], POINTER(c_ulong), 'pdwState' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHelp',
              ( ['retval', 'out'], POINTER(BSTR), 'pszHelp' )),
    COMMETHOD(['propget'], HRESULT, 'CachedKeyboardShortcut',
              ( ['retval', 'out'], POINTER(BSTR), 'pszKeyboardShortcut' )),
    COMMETHOD([], HRESULT, 'GetCachedSelection',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'pvarSelectedChildren' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDefaultAction',
              ( ['retval', 'out'], POINTER(BSTR), 'pszDefaultAction' )),
    COMMETHOD([], HRESULT, 'GetIAccessible',
              ( ['retval', 'out'], POINTER(POINTER(IAccessible)), 'ppAccessible' )),
]



class IUIAutomationItemContainerPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{C690FDB2-27A8-423C-812D-429773C9084E}')
    _idlflags_ = []
    _pid_ = UIA_ItemContainerPatternId
    _vid_ = UIA_IsItemContainerPatternAvailablePropertyId
class IUIAutomationElement(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{D22108AA-8AC5-49A5-837B-37BBB3D7591E}')
    _idlflags_ = []
    
IUIAutomationItemContainerPattern._methods_ = [
    COMMETHOD([], HRESULT, 'FindItemByProperty',
              ( ['in'], POINTER(IUIAutomationElement), 'pStartAfter' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'value' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'pFound' )),
]


UIA_RangeValueMaximumPropertyId = 30050 # Constant c_int
UIA_RangeValueValuePropertyId = 30047 # Constant c_int
UIA_RangeValueLargeChangePropertyId = 30051 # Constant c_int
UIA_RangeValueSmallChangePropertyId = 30052 # Constant c_int
UIA_IsSelectionItemPatternAvailablePropertyId = 30036 # Constant c_int
UIA_ScrollHorizontalScrollPercentPropertyId = 30053 # Constant c_int
UIA_ScrollHorizontalViewSizePropertyId = 30054 # Constant c_int

# values for enumeration 'ScrollAmount'
ScrollAmount_LargeDecrement = 0
ScrollAmount_SmallDecrement = 1
ScrollAmount_NoAmount = 2
ScrollAmount_LargeIncrement = 3
ScrollAmount_SmallIncrement = 4
ScrollAmount = c_int # enum
UIA_ScrollVerticalScrollPercentPropertyId = 30055 # Constant c_int
UIA_ScrollVerticalViewSizePropertyId = 30056 # Constant c_int
UIA_ScrollHorizontallyScrollablePropertyId = 30057 # Constant c_int
UIA_ScrollVerticallyScrollablePropertyId = 30058 # Constant c_int
UIA_LegacyIAccessibleDescriptionPropertyId = 30094 # Constant c_int
UIA_SelectionSelectionPropertyId = 30059 # Constant c_int
UIA_ToolTipClosedEventId = 20001 # Constant c_int
UIA_SelectionIsSelectionRequiredPropertyId = 30061 # Constant c_int
UIA_IsLegacyIAccessiblePatternAvailablePropertyId = 30090 # Constant c_int
UIA_GridColumnCountPropertyId = 30063 # Constant c_int
IAccessible._methods_ = [
    COMMETHOD([dispid(-5000), 'hidden', 'propget'], HRESULT, 'accParent',
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'ppdispParent' )),
    COMMETHOD([dispid(-5001), 'hidden', 'propget'], HRESULT, 'accChildCount',
              ( ['retval', 'out'], POINTER(c_int), 'pcountChildren' )),
    COMMETHOD([dispid(-5002), 'hidden', 'propget'], HRESULT, 'accChild',
              ( ['in'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'ppdispChild' )),
    COMMETHOD([dispid(-5003), 'hidden', 'propget'], HRESULT, 'accName',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszName' )),
    COMMETHOD([dispid(-5004), 'hidden', 'propget'], HRESULT, 'accValue',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszValue' )),
    COMMETHOD([dispid(-5005), 'hidden', 'propget'], HRESULT, 'accDescription',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszDescription' )),
    COMMETHOD([dispid(-5006), 'hidden', 'propget'], HRESULT, 'accRole',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarRole' )),
    COMMETHOD([dispid(-5007), 'hidden', 'propget'], HRESULT, 'accState',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarState' )),
    COMMETHOD([dispid(-5008), 'hidden', 'propget'], HRESULT, 'accHelp',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszHelp' )),
    COMMETHOD([dispid(-5009), 'hidden', 'propget'], HRESULT, 'accHelpTopic',
              ( ['out'], POINTER(BSTR), 'pszHelpFile' ),
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(c_int), 'pidTopic' )),
    COMMETHOD([dispid(-5010), 'hidden', 'propget'], HRESULT, 'accKeyboardShortcut',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszKeyboardShortcut' )),
    COMMETHOD([dispid(-5011), 'hidden', 'propget'], HRESULT, 'accFocus',
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarChild' )),
    COMMETHOD([dispid(-5012), 'hidden', 'propget'], HRESULT, 'accSelection',
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarChildren' )),
    COMMETHOD([dispid(-5013), 'hidden', 'propget'], HRESULT, 'accDefaultAction',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszDefaultAction' )),
    COMMETHOD([dispid(-5014), 'hidden'], HRESULT, 'accSelect',
              ( ['in'], c_int, 'flagsSelect' ),
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5015), 'hidden'], HRESULT, 'accLocation',
              ( ['out'], POINTER(c_int), 'pxLeft' ),
              ( ['out'], POINTER(c_int), 'pyTop' ),
              ( ['out'], POINTER(c_int), 'pcxWidth' ),
              ( ['out'], POINTER(c_int), 'pcyHeight' ),
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5016), 'hidden'], HRESULT, 'accNavigate',
              ( ['in'], c_int, 'navDir' ),
              ( ['in', 'optional'], VARIANT, 'varStart' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarEndUpAt' )),
    COMMETHOD([dispid(-5017), 'hidden'], HRESULT, 'accHitTest',
              ( ['in'], c_int, 'xLeft' ),
              ( ['in'], c_int, 'yTop' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarChild' )),
    COMMETHOD([dispid(-5018), 'hidden'], HRESULT, 'accDoDefaultAction',
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5003), 'hidden', 'propput'], HRESULT, 'accName',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['in'], BSTR, 'pszName' )),
    COMMETHOD([dispid(-5004), 'hidden', 'propput'], HRESULT, 'accValue',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['in'], BSTR, 'pszValue' )),
]



class IUIAutomationCondition(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{352FFBA8-0973-437C-A61F-F64CAFD81DF9}')
    _idlflags_ = []
class IUIAutomationPropertyCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{99EBF2CB-5578-4267-9AD4-AFD6EA77E94B}')
    _idlflags_ = []
IUIAutomationCondition._methods_ = [
]


# values for enumeration 'PropertyConditionFlags'
PropertyConditionFlags_None = 0
PropertyConditionFlags_IgnoreCase = 1
PropertyConditionFlags = c_int # enum
IUIAutomationPropertyCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'propertyId',
              ( ['retval', 'out'], POINTER(c_int), 'propertyId' )),
    COMMETHOD(['propget'], HRESULT, 'PropertyValue',
              ( ['retval', 'out'], POINTER(VARIANT), 'PropertyValue' )),
    COMMETHOD(['propget'], HRESULT, 'PropertyConditionFlags',
              ( ['retval', 'out'], POINTER(PropertyConditionFlags), 'flags' )),
]

UIA_WindowCanMaximizePropertyId = 30073 # Constant c_int
UIA_WindowCanMinimizePropertyId = 30074 # Constant c_int
UIA_WindowWindowVisualStatePropertyId = 30075 # Constant c_int
UIA_WindowWindowInteractionStatePropertyId = 30076 # Constant c_int
UIA_WindowIsModalPropertyId = 30077 # Constant c_int
UIA_TableColumnHeadersPropertyId = 30082 # Constant c_int
UIA_WindowIsTopmostPropertyId = 30078 # Constant c_int
UIA_SelectionItemIsSelectedPropertyId = 30079 # Constant c_int
class IUIAutomationBoolCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{1B4E1F2E-75EB-4D0B-8952-5A69988E2307}')
    _idlflags_ = []
IUIAutomationBoolCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'BooleanValue',
              ( ['retval', 'out'], POINTER(c_int), 'boolVal' )),
]

UIA_RangeValueIsReadOnlyPropertyId = 30048 # Constant c_int
UIA_ScrollPatternId = 10004 # Constant c_int
UIA_RangeValuePatternId = 10003 # Constant c_int

# values for enumeration 'SupportedTextSelection'
SupportedTextSelection_None = 0
SupportedTextSelection_Single = 1
SupportedTextSelection_Multiple = 2
SupportedTextSelection = c_int # enum
UIA_InvokePatternId = 10000 # Constant c_int
UIA_TableItemColumnHeaderItemsPropertyId = 30085 # Constant c_int
UIA_IndentationFirstLineAttributeId = 40010 # Constant c_int
UIA_ControllerForPropertyId = 30104 # Constant c_int
UIA_ExpandCollapsePatternId = 10005 # Constant c_int
UIA_GridPatternId = 10006 # Constant c_int
UIA_GridItemPatternId = 10007 # Constant c_int
UIA_TabControlTypeId = 50018 # Constant c_int
UIA_MultipleViewPatternId = 10008 # Constant c_int
UIA_WindowPatternId = 10009 # Constant c_int
UIA_SelectionItemPatternId = 10010 # Constant c_int
UIA_LegacyIAccessibleValuePropertyId = 30093 # Constant c_int
UIA_TextControlTypeId = 50020 # Constant c_int
UIA_TableItemPatternId = 10013 # Constant c_int
UIA_LegacyIAccessibleStatePropertyId = 30096 # Constant c_int
UIA_TogglePatternId = 10015 # Constant c_int
UIA_LegacyIAccessibleKeyboardShortcutPropertyId = 30098 # Constant c_int
UIA_LegacyIAccessibleSelectionPropertyId = 30099 # Constant c_int
UIA_LegacyIAccessiblePatternId = 10018 # Constant c_int
class IUIAutomationFocusChangedEventHandler(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{C270F6B5-5C69-4290-9745-7A7F97169468}')
    _idlflags_ = ['oleautomation']
IUIAutomationFocusChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleFocusChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' )),
]


UIA_TableRowHeadersPropertyId = 30081 # Constant c_int
UIA_ProviderDescriptionPropertyId = 30107 # Constant c_int
UIA_AnimationStyleAttributeId = 40000 # Constant c_int
class IUIAutomationRangeValuePattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{59213F4F-7346-49E5-B120-80555987A148}')
    _idlflags_ = []
    _pid_ = UIA_RangeValuePatternId
    _vid_ = UIA_IsRangeValuePatternAvailablePropertyId
IUIAutomationRangeValuePattern._methods_ = [
    COMMETHOD([], HRESULT, 'SetValue',
              ( ['in'], c_double, 'val' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentValue',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsReadOnly',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentMaximum',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentMinimum',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLargeChange',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentSmallChange',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedValue',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsReadOnly',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedMaximum',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedMinimum',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLargeChange',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedSmallChange',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
]

UIA_MarginTrailingAttributeId = 40021 # Constant c_int
UIA_TableRowOrColumnMajorPropertyId = 30083 # Constant c_int
UIA_CalendarControlTypeId = 50001 # Constant c_int
UIA_IsSuperscriptAttributeId = 40017 # Constant c_int

# values for enumeration 'OrientationType'
OrientationType_None = 0
OrientationType_Horizontal = 1
OrientationType_Vertical = 2
OrientationType = c_int # enum
UIA_RangeValueMinimumPropertyId = 30049 # Constant c_int
UIA_IsSynchronizedInputPatternAvailablePropertyId = 30110 # Constant c_int
UIA_CheckBoxControlTypeId = 50002 # Constant c_int
UIA_BulletStyleAttributeId = 40002 # Constant c_int
UIA_CapStyleAttributeId = 40003 # Constant c_int
class IUIAutomationTablePattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{620E691C-EA96-4710-A850-754B24CE2417}')
    _idlflags_ = []
    _pid_ = UIA_TablePatternId
    _vid_ = UIA_IsTablePatternAvailablePropertyId

# values for enumeration 'RowOrColumnMajor'
RowOrColumnMajor_RowMajor = 0
RowOrColumnMajor_ColumnMajor = 1
RowOrColumnMajor_Indeterminate = 2
RowOrColumnMajor = c_int # enum
IUIAutomationTablePattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetCurrentRowHeaders',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentColumnHeaders',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRowOrColumnMajor',
              ( ['retval', 'out'], POINTER(RowOrColumnMajor), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedRowHeaders',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedColumnHeaders',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRowOrColumnMajor',
              ( ['retval', 'out'], POINTER(RowOrColumnMajor), 'retVal' )),
]

UIA_FontNameAttributeId = 40005 # Constant c_int
UIA_FontSizeAttributeId = 40006 # Constant c_int
UIA_GridRowCountPropertyId = 30062 # Constant c_int
class IUIAutomationSynchronizedInputPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{2233BE0B-AFB7-448B-9FDA-3B378AA5EAE1}')
    _idlflags_ = []
    _pid_ = UIA_SynchronizedInputPatternId
    _vid_ = UIA_IsSynchronizedInputPatternAvailablePropertyId

# values for enumeration 'SynchronizedInputType'
SynchronizedInputType_KeyUp = 1
SynchronizedInputType_KeyDown = 2
SynchronizedInputType_LeftMouseUp = 4
SynchronizedInputType_LeftMouseDown = 8
SynchronizedInputType_RightMouseUp = 16
SynchronizedInputType_RightMouseDown = 32
SynchronizedInputType = c_int # enum
IUIAutomationSynchronizedInputPattern._methods_ = [
    COMMETHOD([], HRESULT, 'StartListening',
              ( ['in'], SynchronizedInputType, 'inputType' )),
    COMMETHOD([], HRESULT, 'Cancel'),
]

UIA_ForegroundColorAttributeId = 40008 # Constant c_int
UIA_HorizontalTextAlignmentAttributeId = 40009 # Constant c_int
class IUIAutomationTransformPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A9B55844-A55D-4EF0-926D-569C16FF89BB}')
    _idlflags_ = []
    _pid_ = UIA_TransformPatternId
    _vid_ = UIA_IsTransformPatternAvailablePropertyId
IUIAutomationTransformPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Move',
              ( ['in'], c_double, 'x' ),
              ( ['in'], c_double, 'y' )),
    COMMETHOD([], HRESULT, 'Resize',
              ( ['in'], c_double, 'width' ),
              ( ['in'], c_double, 'height' )),
    COMMETHOD([], HRESULT, 'Rotate',
              ( ['in'], c_double, 'degrees' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanMove',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanResize',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanRotate',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanMove',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanResize',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanRotate',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
]

UIA_IndentationLeadingAttributeId = 40011 # Constant c_int
UIA_IsHiddenAttributeId = 40013 # Constant c_int

class IUIAutomationAndCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{A7D0AF36-B912-45FE-9855-091DDC174AEC}')
    _idlflags_ = []
IUIAutomationAndCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ChildCount',
              ( ['retval', 'out'], POINTER(c_int), 'ChildCount' )),
    COMMETHOD([], HRESULT, 'GetChildrenAsNativeArray',
              ( ['out'], POINTER(POINTER(POINTER(IUIAutomationCondition))), 'childArray' ),
              ( ['out'], POINTER(c_int), 'childArrayCount' )),
    COMMETHOD([], HRESULT, 'GetChildren',
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(POINTER(IUIAutomationCondition))), 'childArray' )),
]

UIA_CultureAttributeId = 40004 # Constant c_int
UIA_IsItalicAttributeId = 40014 # Constant c_int
UIA_IsReadOnlyAttributeId = 40015 # Constant c_int
class IUIAutomationOrCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{8753F032-3DB1-47B5-A1FC-6E34A266C712}')
    _idlflags_ = []
IUIAutomationOrCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ChildCount',
              ( ['retval', 'out'], POINTER(c_int), 'ChildCount' )),
    COMMETHOD([], HRESULT, 'GetChildrenAsNativeArray',
              ( ['out'], POINTER(POINTER(POINTER(IUIAutomationCondition))), 'childArray' ),
              ( ['out'], POINTER(c_int), 'childArrayCount' )),
    COMMETHOD([], HRESULT, 'GetChildren',
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(POINTER(IUIAutomationCondition))), 'childArray' )),
]

UIA_IndentationTrailingAttributeId = 40012 # Constant c_int
UIA_MarginBottomAttributeId = 40018 # Constant c_int

# values for enumeration 'TextPatternRangeEndpoint'
TextPatternRangeEndpoint_Start = 0
TextPatternRangeEndpoint_End = 1
TextPatternRangeEndpoint = c_int # enum
UIA_Selection_InvalidatedEventId = 20013 # Constant c_int
UIA_MarginTopAttributeId = 40020 # Constant c_int
class IUIAutomation(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{30CBE57D-D9D0-452A-AB13-7AC5AC4825EE}')
    _idlflags_ = []
    def get_roor_element(self):
        return self.GetRootElement()
class IUIAutomationCacheRequest(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{B32A92B5-BC25-4078-9C08-D7EE95C48E03}')
    _idlflags_ = []
class IUIAutomationTreeWalker(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{4042C624-389C-4AFC-A630-9DF854A541FC}')
    _idlflags_ = []

# values for enumeration 'TreeScope'
TreeScope_Element = 1
TreeScope_Children = 2
TreeScope_Descendants = 4
TreeScope_Parent = 8
TreeScope_Ancestors = 16
TreeScope_Subtree = 7
TreeScope = c_int # enum
class IUIAutomationEventHandler(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{146C3C17-F12E-4E22-8C27-F894B9B79C69}')
    _idlflags_ = ['oleautomation']
class IUIAutomationPropertyChangedEventHandler(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{40CD37D4-C756-4B0C-8C6F-BDDFEEB13B50}')
    _idlflags_ = ['oleautomation']
class IUIAutomationStructureChangedEventHandler(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{E81D1B4E-11C5-42F8-9754-E7036C79F054}')
    _idlflags_ = ['oleautomation']
class IUIAutomationProxyFactoryMapping(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{09E31E18-872D-4873-93D1-1E541EC133FD}')
    _idlflags_ = []
IUIAutomation._methods_ = [
    COMMETHOD([], HRESULT, 'CompareElements',
              ( ['in'], POINTER(IUIAutomationElement), 'el1' ),
              ( ['in'], POINTER(IUIAutomationElement), 'el2' ),
              ( ['retval', 'out'], POINTER(c_int), 'areSame' )),
    COMMETHOD([], HRESULT, 'CompareRuntimeIds',
              ( ['in'], _midlSAFEARRAY(c_int), 'runtimeId1' ),
              ( ['in'], _midlSAFEARRAY(c_int), 'runtimeId2' ),
              ( ['retval', 'out'], POINTER(c_int), 'areSame' )),
    COMMETHOD([], HRESULT, 'GetRootElement',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'root' )),
    COMMETHOD([], HRESULT, 'ElementFromHandle',
              ( ['in'], c_void_p, 'hwnd' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'ElementFromPoint',
              ( ['in'], tagPOINT, 'pt' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'GetFocusedElement',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'GetRootElementBuildCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'root' )),
    COMMETHOD([], HRESULT, 'ElementFromHandleBuildCache',
              ( ['in'], c_void_p, 'hwnd' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'ElementFromPointBuildCache',
              ( ['in'], tagPOINT, 'pt' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'GetFocusedElementBuildCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'CreateTreeWalker',
              ( ['in'], POINTER(IUIAutomationCondition), 'pCondition' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'ControlViewWalker',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'ContentViewWalker',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'RawViewWalker',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'RawViewCondition',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
    COMMETHOD(['propget'], HRESULT, 'ControlViewCondition',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
    COMMETHOD(['propget'], HRESULT, 'ContentViewCondition',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
    COMMETHOD([], HRESULT, 'CreateCacheRequest',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCacheRequest)), 'cacheRequest' )),
    COMMETHOD([], HRESULT, 'CreateTrueCondition',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateFalseCondition',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreatePropertyCondition',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'value' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreatePropertyConditionEx',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'value' ),
              ( ['in'], PropertyConditionFlags, 'flags' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateAndCondition',
              ( ['in'], POINTER(IUIAutomationCondition), 'condition1' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition2' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateAndConditionFromArray',
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateAndConditionFromNativeArray',
              ( ['in'], POINTER(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['in'], c_int, 'conditionCount' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateOrCondition',
              ( ['in'], POINTER(IUIAutomationCondition), 'condition1' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition2' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateOrConditionFromArray',
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateOrConditionFromNativeArray',
              ( ['in'], POINTER(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['in'], c_int, 'conditionCount' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateNotCondition',
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'AddAutomationEventHandler',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveAutomationEventHandler',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddPropertyChangedEventHandlerNativeArray',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationPropertyChangedEventHandler), 'handler' ),
              ( ['in'], POINTER(c_int), 'propertyArray' ),
              ( ['in'], c_int, 'propertyCount' )),
    COMMETHOD([], HRESULT, 'AddPropertyChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationPropertyChangedEventHandler), 'handler' ),
              ( ['in'], _midlSAFEARRAY(c_int), 'propertyArray' )),
    COMMETHOD([], HRESULT, 'RemovePropertyChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationPropertyChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddStructureChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationStructureChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveStructureChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationStructureChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddFocusChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationFocusChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveFocusChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationFocusChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveAllEventHandlers'),
    COMMETHOD([], HRESULT, 'IntNativeArrayToSafeArray',
              ( ['in'], POINTER(c_int), 'array' ),
              ( ['in'], c_int, 'arrayCount' ),
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(c_int)), 'safeArray' )),
    COMMETHOD([], HRESULT, 'IntSafeArrayToNativeArray',
              ( ['in'], _midlSAFEARRAY(c_int), 'intArray' ),
              ( ['out'], POINTER(POINTER(c_int)), 'array' ),
              ( ['retval', 'out'], POINTER(c_int), 'arrayCount' )),
    COMMETHOD([], HRESULT, 'RectToVariant',
              ( ['in'], tagRECT, 'rc' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'var' )),
    COMMETHOD([], HRESULT, 'VariantToRect',
              ( ['in'], VARIANT, 'var' ),
              ( ['retval', 'out'], POINTER(tagRECT), 'rc' )),
    COMMETHOD([], HRESULT, 'SafeArrayToRectNativeArray',
              ( ['in'], _midlSAFEARRAY(c_double), 'rects' ),
              ( ['out'], POINTER(POINTER(tagRECT)), 'rectArray' ),
              ( ['retval', 'out'], POINTER(c_int), 'rectArrayCount' )),
    COMMETHOD([], HRESULT, 'CreateProxyFactoryEntry',
              ( ['in'], POINTER(IUIAutomationProxyFactory), 'factory' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationProxyFactoryEntry)), 'factoryEntry' )),
    COMMETHOD(['propget'], HRESULT, 'ProxyFactoryMapping',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationProxyFactoryMapping)), 'factoryMapping' )),
    COMMETHOD([], HRESULT, 'GetPropertyProgrammaticName',
              ( ['in'], c_int, 'property' ),
              ( ['retval', 'out'], POINTER(BSTR), '_name' )),
    COMMETHOD([], HRESULT, 'GetPatternProgrammaticName',
              ( ['in'], c_int, 'pattern' ),
              ( ['retval', 'out'], POINTER(BSTR), '_name' )),
    COMMETHOD([], HRESULT, 'PollForPotentialSupportedPatterns',
              ( ['in'], POINTER(IUIAutomationElement), 'pElement' ),
              ( ['out'], POINTER(_midlSAFEARRAY(c_int)), 'patternIds' ),
              ( ['out'], POINTER(_midlSAFEARRAY(BSTR)), 'patternNames' )),
    COMMETHOD([], HRESULT, 'PollForPotentialSupportedProperties',
              ( ['in'], POINTER(IUIAutomationElement), 'pElement' ),
              ( ['out'], POINTER(_midlSAFEARRAY(c_int)), 'propertyIds' ),
              ( ['out'], POINTER(_midlSAFEARRAY(BSTR)), 'propertyNames' )),
    COMMETHOD([], HRESULT, 'CheckNotSupported',
              ( ['in'], VARIANT, 'value' ),
              ( ['retval', 'out'], POINTER(c_int), 'isNotSupported' )),
    COMMETHOD(['propget'], HRESULT, 'ReservedNotSupportedValue',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'notSupportedValue' )),
    COMMETHOD(['propget'], HRESULT, 'ReservedMixedAttributeValue',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'mixedAttributeValue' )),
    COMMETHOD([], HRESULT, 'ElementFromIAccessible',
              ( ['in'], POINTER(IAccessible), 'accessible' ),
              ( ['in'], c_int, 'childId' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'ElementFromIAccessibleBuildCache',
              ( ['in'], POINTER(IAccessible), 'accessible' ),
              ( ['in'], c_int, 'childId' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
]

UIA_OutlineStylesAttributeId = 40022 # Constant c_int
IUIAutomationProxyFactoryMapping._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'count',
              ( ['retval', 'out'], POINTER(c_uint), 'count' )),
    COMMETHOD([], HRESULT, 'GetTable',
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(POINTER(IUIAutomationProxyFactoryEntry))), 'table' )),
    COMMETHOD([], HRESULT, 'GetEntry',
              ( ['in'], c_uint, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationProxyFactoryEntry)), 'entry' )),
    COMMETHOD([], HRESULT, 'SetTable',
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationProxyFactoryEntry)), 'factoryList' )),
    COMMETHOD([], HRESULT, 'InsertEntries',
              ( ['in'], c_uint, 'before' ),
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationProxyFactoryEntry)), 'factoryList' )),
    COMMETHOD([], HRESULT, 'InsertEntry',
              ( ['in'], c_uint, 'before' ),
              ( ['in'], POINTER(IUIAutomationProxyFactoryEntry), 'factory' )),
    COMMETHOD([], HRESULT, 'RemoveEntry',
              ( ['in'], c_uint, 'index' )),
    COMMETHOD([], HRESULT, 'ClearTable'),
    COMMETHOD([], HRESULT, 'RestoreDefaultTable'),
]

UIA_CustomControlTypeId = 50025 # Constant c_int

# values for enumeration 'WindowInteractionState'
WindowInteractionState_Running = 0
WindowInteractionState_Closing = 1
WindowInteractionState_ReadyForUserInteraction = 2
WindowInteractionState_BlockedByModalWindow = 3
WindowInteractionState_NotResponding = 4
WindowInteractionState = c_int # enum
UIA_ListControlTypeId = 50008 # Constant c_int
UIA_StrikethroughStyleAttributeId = 40026 # Constant c_int
UIA_TableItemRowHeaderItemsPropertyId = 30084 # Constant c_int
UIA_TabsAttributeId = 40027 # Constant c_int
UIA_TextFlowDirectionsAttributeId = 40028 # Constant c_int

# values for enumeration 'WindowVisualState'
WindowVisualState_Normal = 0
WindowVisualState_Maximized = 1
WindowVisualState_Minimized = 2
WindowVisualState = c_int # enum
UIA_UnderlineColorAttributeId = 40029 # Constant c_int
UIA_UnderlineStyleAttributeId = 40030 # Constant c_int
UIA_ButtonControlTypeId = 50000 # Constant c_int
UIA_IsOffscreenPropertyId = 30022 # Constant c_int
UIA_TransformCanResizePropertyId = 30088 # Constant c_int
UIA_ComboBoxControlTypeId = 50003 # Constant c_int
class IUIAutomationNotCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{F528B657-847B-498C-8896-D52B565407A1}')
    _idlflags_ = []
IUIAutomationNotCondition._methods_ = [
    COMMETHOD([], HRESULT, 'GetChild',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
]


UIA_HyperlinkControlTypeId = 50005 # Constant c_int
UIA_ImageControlTypeId = 50006 # Constant c_int
UIA_ListItemControlTypeId = 50007 # Constant c_int
class IUIAutomationScrollPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{88F4D42A-E881-459D-A77C-73BBBB7E02DC}')
    _idlflags_ = []
    _pid_ = UIA_ScrollPatternId
    _vid_ = UIA_IsScrollPatternAvailablePropertyId
IUIAutomationScrollPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Scroll',
              ( ['in'], ScrollAmount, 'horizontalAmount' ),
              ( ['in'], ScrollAmount, 'verticalAmount' )),
    COMMETHOD([], HRESULT, 'SetScrollPercent',
              ( ['in'], c_double, 'horizontalPercent' ),
              ( ['in'], c_double, 'verticalPercent' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHorizontalScrollPercent',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentVerticalScrollPercent',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHorizontalViewSize',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentVerticalViewSize',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHorizontallyScrollable',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentVerticallyScrollable',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHorizontalScrollPercent',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedVerticalScrollPercent',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHorizontalViewSize',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedVerticalViewSize',
              ( ['retval', 'out'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHorizontallyScrollable',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedVerticallyScrollable',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
]

UIA_MenuControlTypeId = 50009 # Constant c_int
UIA_MenuBarControlTypeId = 50010 # Constant c_int
UIA_MenuItemControlTypeId = 50011 # Constant c_int
UIA_ProgressBarControlTypeId = 50012 # Constant c_int
UIA_RadioButtonControlTypeId = 50013 # Constant c_int
UIA_ScrollBarControlTypeId = 50014 # Constant c_int
UIA_SliderControlTypeId = 50015 # Constant c_int
class IUIAutomationGridPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{414C3CDC-856B-4F5B-8538-3131C6302550}')
    _idlflags_ = []
    _pid_ = UIA_GridPatternId
    _vid_ = UIA_IsGridPatternAvailablePropertyId
IUIAutomationGridPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetItem',
              ( ['in'], c_int, 'row' ),
              ( ['in'], c_int, 'column' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRowCount',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentColumnCount',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRowCount',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedColumnCount',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
]

UIA_SpinnerControlTypeId = 50016 # Constant c_int
UIA_StatusBarControlTypeId = 50017 # Constant c_int
UIA_HasKeyboardFocusPropertyId = 30008 # Constant c_int
UIA_HeaderControlTypeId = 50034 # Constant c_int
IUIAutomationTreeWalker._methods_ = [
    COMMETHOD([], HRESULT, 'GetParentElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'parent' )),
    COMMETHOD([], HRESULT, 'GetFirstChildElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'first' )),
    COMMETHOD([], HRESULT, 'GetLastChildElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'last' )),
    COMMETHOD([], HRESULT, 'GetNextSiblingElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'next' )),
    COMMETHOD([], HRESULT, 'GetPreviousSiblingElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'previous' )),
    COMMETHOD([], HRESULT, 'NormalizeElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'normalized' )),
    COMMETHOD([], HRESULT, 'GetParentElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'parent' )),
    COMMETHOD([], HRESULT, 'GetFirstChildElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'first' )),
    COMMETHOD([], HRESULT, 'GetLastChildElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'last' )),
    COMMETHOD([], HRESULT, 'GetNextSiblingElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'next' )),
    COMMETHOD([], HRESULT, 'GetPreviousSiblingElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'previous' )),
    COMMETHOD([], HRESULT, 'NormalizeElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'normalized' )),
    COMMETHOD(['propget'], HRESULT, 'condition',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
]

UIA_GridItemRowPropertyId = 30064 # Constant c_int
UIA_LegacyIAccessibleChildIdPropertyId = 30091 # Constant c_int
IUIAutomationPropertyChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandlePropertyChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'newValue' )),
]


UIA_ToolBarControlTypeId = 50021 # Constant c_int
UIA_ToolTipControlTypeId = 50022 # Constant c_int
UIA_TreeControlTypeId = 50023 # Constant c_int
UIA_TreeItemControlTypeId = 50024 # Constant c_int
UIA_OverlineColorAttributeId = 40023 # Constant c_int
UIA_GroupControlTypeId = 50026 # Constant c_int
UIA_ThumbControlTypeId = 50027 # Constant c_int
class Library(object):
    _name = u'UIAutomationClient'
    _reg_typelib_ = ('{944DE083-8FB8-45CF-BCB7-C477ACB2F897}', 1, 0)

UIA_DataGridControlTypeId = 50028 # Constant c_int
UIA_DataItemControlTypeId = 50029 # Constant c_int
IUIAutomationEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleAutomationEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], c_int, 'eventId' )),
]


UIA_DocumentControlTypeId = 50030 # Constant c_int
UIA_SplitButtonControlTypeId = 50031 # Constant c_int

# values for enumeration 'AutomationElementMode'
AutomationElementMode_None = 0
AutomationElementMode_Full = 1
AutomationElementMode = c_int # enum
IUIAutomationCacheRequest._methods_ = [
    COMMETHOD([], HRESULT, 'AddProperty',
              ( ['in'], c_int, 'propertyId' )),
    COMMETHOD([], HRESULT, 'AddPattern',
              ( ['in'], c_int, 'patternId' )),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCacheRequest)), 'clonedRequest' )),
    COMMETHOD(['propget'], HRESULT, 'TreeScope',
              ( ['retval', 'out'], POINTER(TreeScope), 'scope' )),
    COMMETHOD(['propput'], HRESULT, 'TreeScope',
              ( ['in'], TreeScope, 'scope' )),
    COMMETHOD(['propget'], HRESULT, 'TreeFilter',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationCondition)), 'filter' )),
    COMMETHOD(['propput'], HRESULT, 'TreeFilter',
              ( ['in'], POINTER(IUIAutomationCondition), 'filter' )),
    COMMETHOD(['propget'], HRESULT, 'AutomationElementMode',
              ( ['retval', 'out'], POINTER(AutomationElementMode), 'mode' )),
    COMMETHOD(['propput'], HRESULT, 'AutomationElementMode',
              ( ['in'], AutomationElementMode, 'mode' )),
]

UIA_WindowControlTypeId = 50032 # Constant c_int
class IUIAutomationWindowPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0FAEF453-9208-43EF-BBB2-3B485177864F}')
    _idlflags_ = []
    _pid_ = UIA_WindowPatternId
    _vid_ = UIA_IsWindowPatternAvailablePropertyId
IUIAutomationWindowPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Close'),
    COMMETHOD([], HRESULT, 'WaitForInputIdle',
              ( ['in'], c_int, 'milliseconds' ),
              ( ['retval', 'out'], POINTER(c_int), 'success' )),
    COMMETHOD([], HRESULT, 'SetWindowVisualState',
              ( ['in'], WindowVisualState, 'state' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanMaximize',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanMinimize',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsModal',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsTopmost',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentWindowVisualState',
              ( ['retval', 'out'], POINTER(WindowVisualState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentWindowInteractionState',
              ( ['retval', 'out'], POINTER(WindowInteractionState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanMaximize',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanMinimize',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsModal',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsTopmost',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedWindowVisualState',
              ( ['retval', 'out'], POINTER(WindowVisualState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedWindowInteractionState',
              ( ['retval', 'out'], POINTER(WindowInteractionState), 'retVal' )),
]

UIA_PaneControlTypeId = 50033 # Constant c_int
UIA_StrikethroughColorAttributeId = 40025 # Constant c_int

# values for enumeration 'TextUnit'
TextUnit_Character = 0
TextUnit_Format = 1
TextUnit_Word = 2
TextUnit_Line = 3
TextUnit_Paragraph = 4
TextUnit_Page = 5
TextUnit_Document = 6
TextUnit = c_int # enum
UIA_TableControlTypeId = 50036 # Constant c_int
UIA_HeaderItemControlTypeId = 50035 # Constant c_int
UIA_TitleBarControlTypeId = 50037 # Constant c_int
UIA_TablePatternId = 10012 # Constant c_int
class IUIAutomationInvokePattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{FB377FBE-8EA6-46D5-9C73-6499642D3059}')
    _idlflags_ = []
    _pid_ = UIA_InvokePatternId
    _vid_ = UIA_IsInvokePatternAvailablePropertyId
IUIAutomationInvokePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Invoke'),
]

# values for enumeration 'StructureChangeType'
StructureChangeType_ChildAdded = 0
StructureChangeType_ChildRemoved = 1
StructureChangeType_ChildrenInvalidated = 2
StructureChangeType_ChildrenBulkAdded = 3
StructureChangeType_ChildrenBulkRemoved = 4
StructureChangeType_ChildrenReordered = 5
StructureChangeType = c_int # enum

# values for enumeration 'ExpandCollapseState'
ExpandCollapseState_Collapsed = 0
ExpandCollapseState_Expanded = 1
ExpandCollapseState_PartiallyExpanded = 2
ExpandCollapseState_LeafNode = 3
ExpandCollapseState = c_int # enum
UIA_SelectionCanSelectMultiplePropertyId = 30060 # Constant c_int

# values for enumeration 'ToggleState'
ToggleState_Off = 0
ToggleState_On = 1
ToggleState_Indeterminate = 2
ToggleState = c_int # enum
UIA_LegacyIAccessibleDefaultActionPropertyId = 30100 # Constant c_int
UIA_MenuModeEndEventId = 20019 # Constant c_int
UIA_TextPatternId = 10014 # Constant c_int
class IUIAutomationScrollItemPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{B488300F-D015-4F19-9C29-BB595E3645EF}')
    _idlflags_ = []
    _pid_ = UIA_ScrollItemPatternId
    _vid_ = UIA_IsScrollItemPatternAvailablePropertyId
IUIAutomationScrollItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'ScrollIntoView'),
]

UIA_ToggleToggleStatePropertyId = 30086 # Constant c_int
UIA_LegacyIAccessibleHelpPropertyId = 30097 # Constant c_int
UIA_FontWeightAttributeId = 40007 # Constant c_int
IUIAutomationElement._methods_ = [
    COMMETHOD([], HRESULT, 'SetFocus'),
    COMMETHOD([], HRESULT, 'GetRuntimeId',
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(c_int)), 'runtimeId' )),
    COMMETHOD([], HRESULT, 'FindFirst',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'found' )),
    COMMETHOD([], HRESULT, 'FindAll',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'found' )),
    COMMETHOD([], HRESULT, 'FindFirstBuildCache',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'found' )),
    COMMETHOD([], HRESULT, 'FindAllBuildCache',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'found' )),
    COMMETHOD([], HRESULT, 'BuildUpdatedCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'updatedElement' )),
    COMMETHOD([], HRESULT, 'GetCurrentPropertyValue',
              ( ['in'], c_int, 'propertyId' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentPropertyValueEx',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], c_int, 'ignoreDefaultValue' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedPropertyValue',
              ( ['in'], c_int, 'propertyId' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedPropertyValueEx',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], c_int, 'ignoreDefaultValue' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentPatternAs',
              ( ['in'], c_int, 'patternId' ),
              ( ['in'], POINTER(GUID), 'riid' ),
              ( ['retval', 'out'], POINTER(c_void_p), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCachedPatternAs',
              ( ['in'], c_int, 'patternId' ),
              ( ['in'], POINTER(GUID), 'riid' ),
              ( ['retval', 'out'], POINTER(c_void_p), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCurrentPattern',
              ( ['in'], c_int, 'patternId' ),
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCachedPattern',
              ( ['in'], c_int, 'patternId' ),
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCachedParent',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'parent' )),
    COMMETHOD([], HRESULT, 'GetCachedChildren',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'children' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentProcessId',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentControlType',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLocalizedControlType',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentName',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAcceleratorKey',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAccessKey',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHasKeyboardFocus',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsKeyboardFocusable',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsEnabled',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAutomationId',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentClassName',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHelpText',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCulture',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsControlElement',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsContentElement',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsPassword',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentNativeWindowHandle',
              ( ['retval', 'out'], POINTER(c_void_p), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentItemType',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsOffscreen',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentOrientation',
              ( ['retval', 'out'], POINTER(OrientationType), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFrameworkId',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsRequiredForForm',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentItemStatus',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentBoundingRectangle',
              ( ['retval', 'out'], POINTER(tagRECT), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLabeledBy',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAriaRole',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAriaProperties',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsDataValidForForm',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentControllerFor',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDescribedBy',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFlowsTo',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentProviderDescription',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedProcessId',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedControlType',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLocalizedControlType',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedName',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAcceleratorKey',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAccessKey',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHasKeyboardFocus',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsKeyboardFocusable',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsEnabled',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAutomationId',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedClassName',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHelpText',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCulture',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsControlElement',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsContentElement',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsPassword',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedNativeWindowHandle',
              ( ['retval', 'out'], POINTER(c_void_p), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedItemType',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsOffscreen',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedOrientation',
              ( ['retval', 'out'], POINTER(OrientationType), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFrameworkId',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsRequiredForForm',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedItemStatus',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedBoundingRectangle',
              ( ['retval', 'out'], POINTER(tagRECT), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLabeledBy',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAriaRole',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAriaProperties',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsDataValidForForm',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedControllerFor',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDescribedBy',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFlowsTo',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedProviderDescription',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetClickablePoint',
              ( ['out'], POINTER(tagPOINT), 'clickable' ),
              ( ['retval', 'out'], POINTER(c_int), 'gotClickable' )),
]

UIA_ClassNamePropertyId = 30012 # Constant c_int
class IUIAutomationTableItemPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0B964EB3-EF2E-4464-9C79-61D61737A27E}')
    _idlflags_ = []
    _pid_ = UIA_TableItemPatternId
    _vid_ = UIA_IsTableItemPatternAvailablePropertyId
IUIAutomationTableItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetCurrentRowHeaderItems',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentColumnHeaderItems',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedRowHeaderItems',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedColumnHeaderItems',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
]

class IUIAutomationGridItemPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{78F8EF57-66C3-4E09-BD7C-E79B2004894D}')
    _idlflags_ = []
    _pid_ = UIA_GridItemPatternId
    _vid_ = UIA_IsGridItemPatternAvailablePropertyId
IUIAutomationGridItemPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentContainingGrid',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRow',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentColumn',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRowSpan',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentColumnSpan',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedContainingGrid',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRow',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedColumn',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRowSpan',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedColumnSpan',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
]


class IUIAutomationSelectionPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{5ED5202E-B2AC-47A6-B638-4B0BF140D78E}')
    _idlflags_ = []
    _pid_ = UIA_SelectionPatternId
    _vid_ = UIA_IsSelectionPatternAvailablePropertyId
IUIAutomationSelectionPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetCurrentSelection',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanSelectMultiple',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsSelectionRequired',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedSelection',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanSelectMultiple',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsSelectionRequired',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
]

class IUIAutomationMultipleViewPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{8D253C91-1DC5-4BB5-B18F-ADE16FA495E8}')
    _idlflags_ = []
    _pid_ = UIA_MultipleViewPatternId
    _vid_ = UIA_IsMultipleViewPatternAvailablePropertyId
IUIAutomationMultipleViewPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetViewName',
              ( ['in'], c_int, 'view' ),
              ( ['retval', 'out'], POINTER(BSTR), '_name' )),
    COMMETHOD([], HRESULT, 'SetCurrentView',
              ( ['in'], c_int, 'view' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCurrentView',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentSupportedViews',
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCurrentView',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedSupportedViews',
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
]

class IUIAutomationValuePattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A94CD8B1-0844-4CD6-9D2D-640537AB39E9}')
    _idlflags_ = []
    _pid_ = UIA_ValuePatternId
    _vid_ = UIA_IsValuePatternAvailablePropertyId
IUIAutomationValuePattern._methods_ = [
    COMMETHOD([], HRESULT, 'SetValue',
              ( ['in'], BSTR, 'val' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentValue',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsReadOnly',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedValue',
              ( ['retval', 'out'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsReadOnly',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
]

class CUIAutomation(CoClass):
    u'The Central Class for UIAutomation'
    _reg_clsid_ = GUID('{FF48DBA4-60EF-4201-AA87-54103EEF594E}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{944DE083-8FB8-45CF-BCB7-C477ACB2F897}', 1, 0)
CUIAutomation._com_interfaces_ = [IUIAutomation]

UIA_LegacyIAccessibleRolePropertyId = 30095 # Constant c_int
IUIAutomationStructureChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleStructureChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], StructureChangeType, 'changeType' ),
              ( ['in'], _midlSAFEARRAY(c_int), 'runtimeId' )),
]



UIA_IsSubscriptAttributeId = 40016 # Constant c_int
class IUIAutomationTextRangeArray(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{CE4AE76A-E717-4C98-81EA-47371D028EB6}')
    _idlflags_ = []
class IUIAutomationTextRange(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A543CC6A-F4AE-494B-8239-C814481187A8}')
    _idlflags_ = []
IUIAutomationTextRangeArray._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'Length',
              ( ['retval', 'out'], POINTER(c_int), 'Length' )),
    COMMETHOD([], HRESULT, 'GetElement',
              ( ['in'], c_int, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRange)), 'element' )),
]

IUIAutomationTextRange._methods_ = [
    COMMETHOD([], HRESULT, 'Clone',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRange)), 'clonedRange' )),
    COMMETHOD([], HRESULT, 'Compare',
              ( ['in'], POINTER(IUIAutomationTextRange), 'range' ),
              ( ['retval', 'out'], POINTER(c_int), 'areSame' )),
    COMMETHOD([], HRESULT, 'CompareEndpoints',
              ( ['in'], TextPatternRangeEndpoint, 'srcEndPoint' ),
              ( ['in'], POINTER(IUIAutomationTextRange), 'range' ),
              ( ['in'], TextPatternRangeEndpoint, 'targetEndPoint' ),
              ( ['retval', 'out'], POINTER(c_int), 'compValue' )),
    COMMETHOD([], HRESULT, 'ExpandToEnclosingUnit',
              ( ['in'], TextUnit, 'TextUnit' )),
    COMMETHOD([], HRESULT, 'FindAttribute',
              ( ['in'], c_int, 'attr' ),
              ( ['in'], VARIANT, 'val' ),
              ( ['in'], c_int, 'backward' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRange)), 'found' )),
    COMMETHOD([], HRESULT, 'FindText',
              ( ['in'], BSTR, 'text' ),
              ( ['in'], c_int, 'backward' ),
              ( ['in'], c_int, 'ignoreCase' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRange)), 'found' )),
    COMMETHOD([], HRESULT, 'GetAttributeValue',
              ( ['in'], c_int, 'attr' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'value' )),
    COMMETHOD([], HRESULT, 'GetBoundingRectangles',
              ( ['retval', 'out'], POINTER(_midlSAFEARRAY(c_double)), 'boundingRects' )),
    COMMETHOD([], HRESULT, 'GetEnclosingElement',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'enclosingElement' )),
    COMMETHOD([], HRESULT, 'GetText',
              ( ['in'], c_int, 'maxLength' ),
              ( ['retval', 'out'], POINTER(BSTR), 'text' )),
    COMMETHOD([], HRESULT, 'Move',
              ( ['in'], TextUnit, 'unit' ),
              ( ['in'], c_int, 'count' ),
              ( ['retval', 'out'], POINTER(c_int), 'moved' )),
    COMMETHOD([], HRESULT, 'MoveEndpointByUnit',
              ( ['in'], TextPatternRangeEndpoint, 'endpoint' ),
              ( ['in'], TextUnit, 'unit' ),
              ( ['in'], c_int, 'count' ),
              ( ['retval', 'out'], POINTER(c_int), 'moved' )),
    COMMETHOD([], HRESULT, 'MoveEndpointByRange',
              ( ['in'], TextPatternRangeEndpoint, 'srcEndPoint' ),
              ( ['in'], POINTER(IUIAutomationTextRange), 'range' ),
              ( ['in'], TextPatternRangeEndpoint, 'targetEndPoint' )),
    COMMETHOD([], HRESULT, 'Select'),
    COMMETHOD([], HRESULT, 'AddToSelection'),
    COMMETHOD([], HRESULT, 'RemoveFromSelection'),
    COMMETHOD([], HRESULT, 'ScrollIntoView',
              ( ['in'], c_int, 'alignToTop' )),
    COMMETHOD([], HRESULT, 'GetChildren',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElementArray)), 'children' )),
]


UIA_AriaRolePropertyId = 30101 # Constant c_int
class IUIAutomationSelectionItemPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A8EFA66A-0FDA-421A-9194-38021F3578EA}')
    _idlflags_ = []
    _pid_ = UIA_SelectionItemPatternId
    _vid_ = UIA_IsSelectionItemPatternAvailablePropertyId
IUIAutomationSelectionItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Select'),
    COMMETHOD([], HRESULT, 'AddToSelection'),
    COMMETHOD([], HRESULT, 'RemoveFromSelection'),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsSelected',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentSelectionContainer',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsSelected',
              ( ['retval', 'out'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedSelectionContainer',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
]


class IUIAutomationTextPattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{32EBA289-3583-42C9-9C59-3B6D9A1E9B6A}')
    _idlflags_ = []
    _pid_ = UIA_TextPatternId
    _vid_ = UIA_IsTextPatternAvailablePropertyId
IUIAutomationTextPattern._methods_ = [
    COMMETHOD([], HRESULT, 'RangeFromPoint',
              ( ['in'], tagPOINT, 'pt' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD([], HRESULT, 'RangeFromChild',
              ( ['in'], POINTER(IUIAutomationElement), 'child' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD([], HRESULT, 'GetSelection',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRangeArray)), 'ranges' )),
    COMMETHOD([], HRESULT, 'GetVisibleRanges',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRangeArray)), 'ranges' )),
    COMMETHOD(['propget'], HRESULT, 'DocumentRange',
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD(['propget'], HRESULT, 'SupportedTextSelection',
              ( ['retval', 'out'], POINTER(SupportedTextSelection), 'SupportedTextSelection' )),
]

IUIAutomationElementArray._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'Length',
              ( ['retval', 'out'], POINTER(c_int), 'Length' )),
    COMMETHOD([], HRESULT, 'GetElement',
              ( ['in'], c_int, 'index' ),
              ( ['retval', 'out'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
]

class IUIAutomationTogglePattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{94CF8058-9B8D-4AB9-8BFD-4CD0A33C8C70}')
    _idlflags_ = []
    _pid_ = UIA_TogglePatternId
    _vid_ = UIA_IsTogglePatternAvailablePropertyId
IUIAutomationTogglePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Toggle'),
    COMMETHOD(['propget'], HRESULT, 'CurrentToggleState',
              ( ['retval', 'out'], POINTER(ToggleState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedToggleState',
              ( ['retval', 'out'], POINTER(ToggleState), 'retVal' )),
]

class IUIAutomationExpandCollapsePattern(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{619BE086-1F4E-4EE4-BAFA-210128738730}')
    _idlflags_ = []
    _pid_ = UIA_ExpandCollapsePatternId
    _vid_ = UIA_IsExpandCollapsePatternAvailablePropertyId
IUIAutomationExpandCollapsePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Expand'),
    COMMETHOD([], HRESULT, 'Collapse'),
    COMMETHOD(['propget'], HRESULT, 'CurrentExpandCollapseState',
              ( ['retval', 'out'], POINTER(ExpandCollapseState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedExpandCollapseState',
              ( ['retval', 'out'], POINTER(ExpandCollapseState), 'retVal' )),
]

__all__ = ['UIA_IsGridItemPatternAvailablePropertyId',
           'IUIAutomationAndCondition',
           'UIA_StrikethroughColorAttributeId',
           'UIA_LegacyIAccessiblePatternId', 'IUIAutomationElement',
           'UIA_ClickablePointPropertyId',
           'WindowVisualState_Maximized',
           'WindowInteractionState_Running',
           'UIA_SliderControlTypeId',
           'UIA_ForegroundColorAttributeId',
           'UIA_HeaderControlTypeId', 'UIA_ScrollItemPatternId',
           'UIA_Invoke_InvokedEventId', 'UIA_HyperlinkControlTypeId',
           'UIA_Window_WindowOpenedEventId', 'OrientationType_None',
           'UIA_ValueIsReadOnlyPropertyId',
           'PropertyConditionFlags_None', 'UIA_ToolTipControlTypeId',
           'UIA_MultipleViewCurrentViewPropertyId',
           'UIA_MarginLeadingAttributeId',
           'UIA_GridColumnCountPropertyId', 'UIA_WindowControlTypeId',
           'UIA_CheckBoxControlTypeId',
           'UIA_SelectionItem_ElementAddedToSelectionEventId',
           'UIA_OutlineStylesAttributeId',
           'UIA_LegacyIAccessibleRolePropertyId',
           'UIA_InputReachedOtherElementEventId',
           'UIA_SelectionItem_ElementRemovedFromSelectionEventId',
           'IUIAutomationExpandCollapsePattern', 'DockPosition_None',
           'SynchronizedInputType_LeftMouseUp',
           'UIA_LegacyIAccessibleDefaultActionPropertyId',
           'UIA_IsMultipleViewPatternAvailablePropertyId',
           'UIA_RangeValueMinimumPropertyId',
           'UIA_MenuBarControlTypeId', 'UIA_ImageControlTypeId',
           'UIA_DocumentControlTypeId', 'UIA_CustomControlTypeId',
           'UIA_ExpandCollapsePatternId',
           'UIA_GridItemColumnPropertyId',
           'WindowInteractionState_BlockedByModalWindow',
           'IUIAutomationTextRangeArray',
           'StructureChangeType_ChildrenReordered',
           'UIA_SynchronizedInputPatternId',
           'UIA_TreeItemControlTypeId', 'UIA_InvokePatternId',
           'UIA_SelectionItem_ElementSelectedEventId',
           'IUIAutomationWindowPattern', 'AutomationElementMode_None',
           'UIA_IsSelectionItemPatternAvailablePropertyId',
           'UIA_BackgroundColorAttributeId',
           'UIA_AnimationStyleAttributeId',
           'IUIAutomationNotCondition',
           'IUIAutomationTransformPattern',
           'UIA_InputDiscardedEventId',
           'ExpandCollapseState_Expanded', 'UIA_IsItalicAttributeId',
           'UIA_TabItemControlTypeId', 'UIA_DataGridControlTypeId',
           'UIA_DockDockPositionPropertyId',
           'IUIAutomationTextPattern',
           'UIA_IsExpandCollapsePatternAvailablePropertyId',
           'IUIAutomationTreeWalker', 'UIA_LayoutInvalidatedEventId',
           'UIA_LegacyIAccessibleStatePropertyId',
           'UIA_TextPatternId', 'UIA_RangeValueSmallChangePropertyId',
           'UIA_ValueValuePropertyId', 'UIA_SpinnerControlTypeId',
           'UIA_NativeWindowHandlePropertyId',
           'UIA_RuntimeIdPropertyId', 'TextUnit_Document',
           'TextUnit_Word', 'IUIAutomationSynchronizedInputPattern',
           'UIA_TableRowHeadersPropertyId', 'UIA_SelectionPatternId',
           'IUIAutomationOrCondition',
           'WindowInteractionState_Closing',
           'UIA_LegacyIAccessibleNamePropertyId',
           'UIA_TogglePatternId',
           'SynchronizedInputType_RightMouseDown',
           'UIA_RangeValueMaximumPropertyId',
           'IUIAutomationValuePattern',
           'UIA_BoundingRectanglePropertyId',
           'IUIAutomationEventHandler',
           'UIA_TextFlowDirectionsAttributeId',
           'UIA_MultipleViewPatternId',
           'UIA_WindowIsTopmostPropertyId',
           'UIA_Text_TextSelectionChangedEventId',
           'IUIAutomationSelectionPattern', 'UIA_TableControlTypeId',
           'UIA_TableColumnHeadersPropertyId',
           'TextPatternRangeEndpoint_Start',
           'UIA_TableItemColumnHeaderItemsPropertyId',
           'SupportedTextSelection_Single', 'SynchronizedInputType',
           'UIA_ClassNamePropertyId', 'UIA_UnderlineStyleAttributeId',
           'UIA_IsSuperscriptAttributeId',
           'UIA_RangeValueValuePropertyId',
           'UIA_HorizontalTextAlignmentAttributeId',
           'UIA_SelectionItemSelectionContainerPropertyId',
           'UIA_LegacyIAccessibleKeyboardShortcutPropertyId',
           'UIA_IsEnabledPropertyId', 'UIA_PaneControlTypeId',
           'UIA_LocalizedControlTypePropertyId',
           'UIA_GridItemPatternId',
           'IUIAutomationProxyFactoryMapping',
           'WindowVisualState_Normal',
           'UIA_WindowWindowVisualStatePropertyId',
           'ExpandCollapseState_Collapsed',
           'ProviderOptions_OverrideProvider',
           'UIA_MenuClosedEventId', 'UIA_WindowPatternId',
           'UIA_IsSelectionPatternAvailablePropertyId',
           'IUIAutomationDockPattern',
           'IUIAutomationFocusChangedEventHandler',
           'UIA_CalendarControlTypeId', 'TextUnit_Format',
           'UIA_MenuOpenedEventId',
           'UIA_WindowWindowInteractionStatePropertyId',
           'UIA_ToggleToggleStatePropertyId',
           'UIA_IsSynchronizedInputPatternAvailablePropertyId',
           'AutomationElementMode',
           'UIA_SelectionIsSelectionRequiredPropertyId',
           'UIA_ListItemControlTypeId',
           'UIA_LegacyIAccessibleSelectionPropertyId',
           'UIA_TransformPatternId',
           'UIA_IndentationLeadingAttributeId',
           'IUIAutomationTogglePattern',
           'UIA_IsValuePatternAvailablePropertyId',
           'IUIAutomationRangeValuePattern',
           'UIA_ComboBoxControlTypeId', 'UIA_MarginBottomAttributeId',
           'ToggleState_On', 'UIA_DockPatternId',
           'UIA_IsRequiredForFormPropertyId', 'TextUnit_Line',
           'UIA_IsGridPatternAvailablePropertyId',
           'UIA_IsHiddenAttributeId',
           'UIA_TableRowOrColumnMajorPropertyId',
           'TreeScope_Children',
           'WindowInteractionState_ReadyForUserInteraction',
           'IUIAutomation',
           'UIA_SelectionCanSelectMultiplePropertyId',
           'WindowInteractionState_NotResponding',
           'ExpandCollapseState_LeafNode', 'UIA_ToolBarControlTypeId',
           'UIA_TableItemRowHeaderItemsPropertyId',
           'TreeScope_Parent', 'IUIAutomationProxyFactory',
           'ProviderOptions_ClientSideProvider',
           'ScrollAmount_SmallIncrement',
           'ProviderOptions_ProviderOwnsSetFocus',
           'UIA_FontNameAttributeId', 'TreeScope_Element',
           'WindowInteractionState',
           'UIA_IsInvokePatternAvailablePropertyId',
           'ExpandCollapseState',
           'SynchronizedInputType_RightMouseUp',
           'UIA_StrikethroughStyleAttributeId', 'ScrollAmount',
           'UIA_AutomationPropertyChangedEventId',
           'UIA_ExpandCollapseExpandCollapseStatePropertyId',
           'DockPosition_Right', 'UIA_ProgressBarControlTypeId',
           'UIA_ToolTipClosedEventId', 'UIA_MenuModeEndEventId',
           'IUIAutomationPropertyCondition', 'UIA_AriaRolePropertyId',
           'UIA_TransformCanResizePropertyId',
           'AutomationElementMode_Full',
           'StructureChangeType_ChildrenBulkRemoved',
           'UIA_ItemStatusPropertyId', 'UIA_MenuControlTypeId',
           'UIA_ScrollBarControlTypeId',
           'UIA_SelectionItemIsSelectedPropertyId',
           'UIA_CapStyleAttributeId', 'UIA_CultureAttributeId',
           'UIA_ScrollHorizontalScrollPercentPropertyId',
           'UIA_ItemContainerPatternId', 'WindowVisualState',
           'UIA_FlowsToPropertyId', 'UIA_HeaderItemControlTypeId',
           'UIA_ListControlTypeId', 'TextUnit',
           'UIA_ProviderDescriptionPropertyId',
           'UIA_ScrollVerticalViewSizePropertyId',
           'StructureChangeType', 'UIA_SeparatorControlTypeId',
           'UIA_IsContentElementPropertyId',
           'ScrollAmount_LargeDecrement',
           'UIA_MarginTrailingAttributeId',
           'UIA_InputReachedTargetEventId', 'DockPosition_Top',
           'UIA_OrientationPropertyId', 'IUIAutomationCondition',
           'UIA_StructureChangedEventId', 'UIA_MenuItemControlTypeId',
           'UIA_Window_WindowClosedEventId',
           'UIA_FontWeightAttributeId', 'DockPosition_Left',
           'UIA_SelectionSelectionPropertyId',
           'SynchronizedInputType_KeyUp',
           'UIA_StatusBarControlTypeId',
           'UIA_TransformCanRotatePropertyId',
           'UIA_AutomationIdPropertyId',
           'UIA_LegacyIAccessibleChildIdPropertyId',
           'IUIAutomationTableItemPattern',
           'TextPatternRangeEndpoint_End',
           'ProviderOptions_ServerSideProvider',
           'IUIAutomationTextRange', 'ToggleState_Off',
           'UIA_IsWindowPatternAvailablePropertyId',
           'UIA_RangeValueIsReadOnlyPropertyId', 'IAccessible',
           'ToggleState', 'ProviderOptions_UseComThreading',
           'OrientationType_Vertical', 'UIA_TreeControlTypeId',
           'UIA_WindowCanMinimizePropertyId', 'OrientationType',
           'UIA_ControllerForPropertyId', 'TreeScope_Subtree',
           'UIA_GridRowCountPropertyId', 'UIA_IsOffscreenPropertyId',
           'UIA_LegacyIAccessibleDescriptionPropertyId',
           'SupportedTextSelection_None', 'UIA_ValuePatternId',
           'UIA_CulturePropertyId',
           'UIA_IsTableItemPatternAvailablePropertyId',
           'UIA_IsLegacyIAccessiblePatternAvailablePropertyId',
           'TextUnit_Page', 'UIA_NamePropertyId',
           'UIA_FontSizeAttributeId', 'IUIAutomationScrollPattern',
           'UIA_IsReadOnlyAttributeId', 'SupportedTextSelection',
           'UIA_AcceleratorKeyPropertyId', 'CUIAutomation',
           'UIA_TransformCanMovePropertyId',
           'IUIAutomationMultipleViewPattern', 'UIA_ScrollPatternId',
           'UIA_TextControlTypeId',
           'UIA_IsTransformPatternAvailablePropertyId',
           'WindowVisualState_Minimized', 'IUIAutomationCacheRequest',
           'UIA_VirtualizedItemPatternId', 'UIA_ButtonControlTypeId',
           'UIA_IsPasswordPropertyId',
           'SynchronizedInputType_KeyDown',
           'UIA_SelectionItemPatternId', 'PropertyConditionFlags',
           'UIA_UnderlineColorAttributeId',
           'UIA_DataItemControlTypeId',
           'RowOrColumnMajor_ColumnMajor',
           'UIA_MultipleViewSupportedViewsPropertyId',
           'IUIAutomationStructureChangedEventHandler',
           'UIA_IndentationTrailingAttributeId',
           'UIA_ToolTipOpenedEventId', 'TreeScope',
           'IUIAutomationBoolCondition',
           'ScrollAmount_LargeIncrement', 'UIA_ThumbControlTypeId',
           'UIA_GridItemContainingGridPropertyId',
           'UIA_OverlineColorAttributeId',
           'IUIAutomationItemContainerPattern',
           'UIA_IsTablePatternAvailablePropertyId',
           'UIA_GridItemColumnSpanPropertyId',
           'TextPatternRangeEndpoint', 'RowOrColumnMajor_RowMajor',
           'UIA_IsKeyboardFocusablePropertyId',
           'UIA_EditControlTypeId', 'UIA_WindowCanMaximizePropertyId',
           'TextUnit_Paragraph', 'UIA_MenuModeStartEventId',
           'DockPosition', 'ExpandCollapseState_PartiallyExpanded',
           'IRawElementProviderSimple', 'UIA_TablePatternId',
           'UIA_AutomationFocusChangedEventId',
           'UIA_Selection_InvalidatedEventId', 'ProviderOptions',
           'StructureChangeType_ChildRemoved',
           'UIA_GridItemRowSpanPropertyId',
           'UIA_IsRangeValuePatternAvailablePropertyId',
           'SynchronizedInputType_LeftMouseDown',
           'DockPosition_Bottom', 'UIA_Text_TextChangedEventId',
           'IUIAutomationElementArray', 'OrientationType_Horizontal',
           'ProviderOptions_NonClientAreaProvider',
           'IUIAutomationSelectionItemPattern',
           'UIA_DescribedByPropertyId', 'ToggleState_Indeterminate',
           'UIA_LabeledByPropertyId',
           'IUIAutomationPropertyChangedEventHandler',
           'IUIAutomationProxyFactoryEntry',
           'UIA_IsControlElementPropertyId',
           'UIA_RangeValueLargeChangePropertyId',
           'TreeScope_Ancestors', 'UIA_RadioButtonControlTypeId',
           'UIA_IsDataValidForFormPropertyId',
           'UIA_TitleBarControlTypeId', 'IUIAutomationInvokePattern',
           'UIA_RangeValuePatternId', 'UIA_ControlTypePropertyId',
           'UIA_BulletStyleAttributeId', 'UIA_MarginTopAttributeId',
           'IUIAutomationGridPattern', 'DockPosition_Fill',
           'UIA_HasKeyboardFocusPropertyId',
           'UIA_IsTextPatternAvailablePropertyId',
           'UIA_ScrollVerticalScrollPercentPropertyId',
           'UIA_ScrollHorizontalViewSizePropertyId',
           'IUIAutomationScrollItemPattern',
           'UIA_IsSubscriptAttributeId',
           'UIA_IsScrollPatternAvailablePropertyId',
           'ScrollAmount_SmallDecrement',
           'UIA_SplitButtonControlTypeId',
           'UIA_LegacyIAccessibleValuePropertyId',
           'UIA_IsItemContainerPatternAvailablePropertyId',
           'UIA_IsDockPatternAvailablePropertyId',
           'IUIAutomationVirtualizedItemPattern',
           'UIA_AsyncContentLoadedEventId', 'TextUnit_Character',
           'UIA_FrameworkIdPropertyId', 'UIA_TableItemPatternId',
           'TreeScope_Descendants', 'RowOrColumnMajor_Indeterminate',
           'IUIAutomationGridItemPattern', 'UIA_TabsAttributeId',
           'StructureChangeType_ChildrenInvalidated',
           'IUIAutomationTablePattern',
           'PropertyConditionFlags_IgnoreCase',
           'UIA_IsTogglePatternAvailablePropertyId',
           'UIA_IsScrollItemPatternAvailablePropertyId',
           'UIA_GridItemRowPropertyId',
           'UIA_ScrollVerticallyScrollablePropertyId',
           'UIA_AriaPropertiesPropertyId',
           'UIA_WindowIsModalPropertyId',
           'UIA_IsVirtualizedItemPatternAvailablePropertyId',
           'ScrollAmount_NoAmount', 'RowOrColumnMajor',
           'UIA_ItemTypePropertyId',
           'SupportedTextSelection_Multiple',
           'UIA_HelpTextPropertyId',
           'UIA_LegacyIAccessibleHelpPropertyId',
           'UIA_AccessKeyPropertyId',
           'StructureChangeType_ChildAdded',
           'IUIAutomationLegacyIAccessiblePattern',
           'StructureChangeType_ChildrenBulkAdded',
           'UIA_IndentationFirstLineAttributeId',
           'UIA_GroupControlTypeId', 'UIA_ProcessIdPropertyId',
           'UIA_OverlineStyleAttributeId',
           'UIA_ScrollHorizontallyScrollablePropertyId',
           'UIA_TabControlTypeId', 'UIA_GridPatternId']
_check_version('501')