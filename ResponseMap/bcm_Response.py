#coding:utf-8

from ResponseMap.Can_Map import *
import tornado
import Common.CommonVar
import time

def send_Challenge_Dict(data, *args, **args_dict):
    msg = args_dict.get('Msg').get('DATA')
    # if msg[3] == '00':
    #     args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01']['DATA'] = '0000000000000000'
    # else:
    Common.CommonVar.BCM_AUTH = msg
    send_msg = handle_msg(data,args_dict.get('Msg'))
    args_dict.get('sendMsg')(send_msg)


# @tornado.gen.coroutine
def send_ChallResponse_Dict(data04,data06, **args_dict):
    if Common.CommonVar.BCM_AUTH[2] == '11':
        if Common.CommonVar.BCM_AUTH[3] == '00':
            # args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01'] = \
                # args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01_RmtACReq_00']
            # args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01_RmtACReq_12']['count'] = 0
            args_dict.get('self').bcmMsg['GW_hsc5_09']['DATA'] = \
                args_dict.get('self').bcmMsg['GW_hsc5_09_RVS_Status_00']['DATA']
            args_dict.get('self').bcmMsg['GW_hsc5_00']['DATA'] = \
                args_dict.get('self').bcmMsg['GW_hsc5_00_engin_close']['DATA']
        else:
            send_msg04 = handle_msg(data04,args_dict.get('Msg'))
            send_msg04.get('DATA')[2] = '01'
            args_dict.get('sendMsg')(send_msg04)
            time.sleep(0.1)
            args_dict.get('self').bcmMsg['GW_hsc5_09']['DATA'] = \
                args_dict.get('self').bcmMsg['GW_hsc5_09_RVS_Status_01']['DATA']
            args_dict.get('self').bcmMsg['GW_hsc5_00']['DATA'] = \
                args_dict.get('self').bcmMsg['GW_hsc5_00_engin_Run_01']['DATA']

            send_msg06 = handle_msg(data06, args_dict.get('Msg'))
            send_msg06.get('DATA')[2] = '02'
            args_dict.get('sendMsg')(send_msg06)
            time.sleep(0.1)
            args_dict.get('sendMsg')(send_msg06)
            time.sleep(1)
            args_dict.get('sendMsg')(send_msg06)
            time.sleep(1)
            args_dict.get('sendMsg')(send_msg06)
            # args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01'] = \
            #     args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01_RmtACReq_12']
            # args_dict.get('self').Timing_send('TBOX_HSC5_FrP01_RmtACReq_12')
            # args_dict.get('sendMsg')(args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01_RmtACReq_12'])
            # args_dict.get('self').Timing_send_can(send_msg06)



            send_msg06['DATA'][2] = '03'
            # args_dict.get('self').Timing_send_can(send_msg06,0,count=1,delaytime=600)
            args_dict.get('self').Timing_send_can(send_msg06, 0, count=1, delaytime=1)


            # args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01_RmtACReq_12']['count'] = 0
        #args_dict.get('self').WriteFrame(send_msg06)
        # args_dict.get('self').bcmMsg['GW_hsc5_00']['DATA'] = '0000000000000000'
        # args_dict.get('self').bcmMsg['GW_hsc5_09']['DATA'] = '0000000000000000'
        # args_dict.get('self').bcmMsg['TBOX_HSC5_FrP01']['DATA'] = '0000000000000000'
        #dict.get('sendMsg')(send_msg06)
    elif Common.CommonVar.BCM_AUTH[2] == '01':
        send_msg04 = handle_msg(data04, args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg04)
        time.sleep(0.01)
        args_dict.get('self').bcmMsg['GW_hsc5_04']['data'] = \
        args_dict.get('self').bcmMsg['GW_hsc5_04_lock']['data']
        send_msg06 = handle_msg(data06, args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg06)

    elif Common.CommonVar.BCM_AUTH[2] == '02':
        send_msg04 = handle_msg(data04, args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg04)
        time.sleep(0.01)
        # args_dict.get('self').bcmMsg['GW_hsc5_04'] = \
        # args_dict.get('self').bcmMsg['GW_hsc5_04_open']
        send_msg06 = handle_msg(data06, args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg06)

    elif Common.CommonVar.BCM_AUTH[2] == '00':
        send_msg04 = handle_msg(data04, args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg04)
        time.sleep(0.01)
        send_msg06 = handle_msg(data06, args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg06)

    else:


        send_msg04 = handle_msg(data04,args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg04)
        time.sleep(0.01)

        send_msg06 = handle_msg(data06, args_dict.get('Msg'))
        args_dict.get('sendMsg')(send_msg06)

def get_handle(msg, *args, **args_dict):
    return [msg.get('DATA')[1]]

def get_challenge(msg, *args, **args_dict):
    return ['11', '22', '33', '44', '55', '66']


def handle_msg(map_dict, msg):
    sendmsg = {}
    sendmsg['ID'] = map_dict.get('ID')
    sendmsg['DATA'] = []
    for line in map_dict.get('DATA'):
        if 'get' not in line:
            sendmsg['DATA'].append(line)
        else:
            result = eval(line)(msg)
            sendmsg['DATA'] = sendmsg['DATA']+result
    if len(sendmsg['DATA']) < 8:
        sendmsg['DATA'] = sendmsg['DATA'] + ['00']*(8-len(sendmsg['DATA']))
    return sendmsg

def sendNone():
    pass

def sendSafeResponse(msg, *args, **args_dict):
    sendmsg = {}
    sendmsg['ID'] = msg.get('ID')
    sendmsg['DATA'] = msg.get('DATA')
    args_dict.get('sendMsg')(sendmsg)
