
import _keyboard_helper as _helper

def keyup(key):
    '''send special character  up'''
    li = _helper.parse_keys(key)
    for item in li:
        _helper.inputvkchar(_helper.keyboard_vkcode[_helper.specialchartovk[item]],False)
    

def keydown(key):
    '''send special character  down'''
    li = _helper.parse_keys(key)
    for item in li:
        _helper.inputvkchar(_helper.keyboard_vkcode[_helper.specialchartovk[item]],True)
    

def sendkeys(keys):
    li = _helper.parse_keys(_helper.decode_key(keys))
    for item in li:
        if _helper.specialchartovk.get(item,None) != None :
            _helper.sendspecialchar(item)
            continue
        _helper.inputunicodechar(ord(item),True)
        _helper.inputunicodechar(ord(item),False)
 