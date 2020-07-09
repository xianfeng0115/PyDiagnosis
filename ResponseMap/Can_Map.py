#coding:utf-8

from ResponseMap.bcm_Response import *

Challenge_Dict = {'ID':'21','DATA':['02', 'get_handle', 'get_challenge']}
"""
'0x01 = Pending
'0x02 = Feature Active (executed) '0x03 = Completed
'0xF0':' Failed
"""
ChallResponse_Dict = {'ID':'21','DATA':['04', 'get_handle', '02']}
ChallComplate_Dict = {'ID':'21','DATA':['06', 'get_handle', '03']}
BCMRequestType_Dict = {
'0x00' :'Horn/Lights',
'0x01' : 'Lock',
'0x02' : 'Unlock',
'0x03' : 'Windows',
'0x04' : 'Manage Key',
'0x11' : 'Engin0e'
}
Lights_enum = {}
FMURequestParameters_Dict = {
    '00':
        ['Lights_enum',
         '000000',
         'get_Horn',
         '000000'
         'get_time',
         '00000000000000000000',
         ],
    }


#bcm接收报文映射关系
bcm_map = {
    ('40','01'):[send_Challenge_Dict,Challenge_Dict],
    ('40','03'):[send_ChallResponse_Dict,ChallResponse_Dict,ChallComplate_Dict],
}
