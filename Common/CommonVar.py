# coding:utf-8

DBUSER_KEY = 'root'
DBPWD_KEY = 'lujinlei'
DBHOST_KEY = 'localhost'
DBPORT_KEY = '3306'
DBNAME_KEY = 'autotest'
MPU_NAME = "root"
MPU_PWD = "Dgyus@312893"

#加密数据
scEncryReqData = None
#加密明文
plaintext = None

loop = None
BASE = None
Session = None
ENGINE = None
logger = None
AvnData = None

strip = None
port = None

WAN_STATUE = {'00': '无网络', '01': 'Circuit switch', '02': '2G在线', '03': '3G在线', '04': '4G在线', '05': '5G在线'}

NET_TYPE = {0: 'No service', 1: 'GSM', 2: 'WCDMA', 3: 'CDMA', 4: 'EVDO', 5: 'TDSCDMA', 6: 'LTE', 7: 'UNKNOWN'}

CELL_TYPE = {0: '相邻小区', 1: '当前小区'}

ACTIVE_STATUE = {0: '未激活', 1: '已激活'}

ROAMING_SETTING = {0: '不允许漫游', 1: '允许漫游'}

PRIVACY_MODE = {0: '不允许搜集用户私有数据', 1: '允许搜集用户私有数据'}

CALL_STATUE = {0:'无通话',1:'正在建立通话连接',2:'正在发送通话信息',3:'通话已经建立',4:'建立通话失败',
               5:'通话结束',6:'通话连接建立失败，正在重新连接',7:'电话呼入'}

ROAMING_STATUE = {0: '当前非漫游', 1: '当前处于漫游'}

USBI_CMD_DICT = {'GPS信息':'0101','基站信息':'0102','激活信息':'0103','WAN连接信息':'0104','IMSI':'0105',
                 '漫游设置':'0106','用户私有数据设置':'0107','信号强度':'0108','蓝牙钥匙信息':'0109','机械钥匙信息':'010a',
                 '通话状态':'010b','用户Token':'010c','漫游状态':'010d','TBOX版本信息':'010f','查询WIFI功能':'0111',
                 'WIFI连接列表查询':'0112','串码信息':'0113','V2X功能状态':'0007','智能道路信息':'0005'}


NO_DISPLAY = ["satellitesInfo", "基站信息", "SVT_APP激活状态", "在线娱乐APP激活状态", "旅途日志APP激活状态",
              "车辆状态APP激活状态", "iCall_APP激活状态", "bCall_APP激活状态", "Remote_Charge_APP激活状态",
              "大数据APP激活状态", "未激活", "远程诊断APP激活状态", "蓝牙钥匙APP激活状态",'5G网络激活状态','iBOX 5G网络激活状态']

SINGLE = {10:'一格',20:'两格',30:'三格',99:'无信号'}

BCM_AUTH = None

REMOTE_REFLASH_INFO = {
    'ReflashReqInfo': {0: 'Reserved', 1: "可选升级", 2: "强制升级"},
    'ECU_TYPE': {'00': 'Reserved', '01': 'to C', '02': 'to B'}
}

CHARGE_FLAG = {0: '不需要', 1: '需要'}

EnterPermission = {1: '不允许AVN进入刷新模式', 2: '允许AVN进入刷新模式'}

TelematicsCfgStatusUpdate = {'Status': {0: "Reserved", 1: "正在连接配置服务器",
                                        2: "无需升级配置（当前配置已经是最新）",
                                        3:"正在升级配置", 4: "配置升级成功", 5: "配置升级失败"},

}
RemoteReflashCheckUpdate = {
    'Status': { "00":"Reserved", "01":"没有更新", "02":"发现更新，正在后台下载", "03":"下载完成，正在比对物流数据",
                "04":"正在安装", "05":"存在安装包未安装", "06":"存在安装包且上一次安装失败", "07":"正在检查更新",
                "20":"网络异常", "21":"TBOX ID不存在（服务器返回 error code 400）",
                "22":"服务器内部错误（服务器返回 error code 500）", "23":"访问地址不存在（服务器返回 error code 404）",
                "24":"没有该 VIN对应的车辆（服务器返回 error code 16570）",
                "25":"有多个 FLID 和 VIN 关联（服务器返回 error code 16571）",
                "26":"没有该 VIN对应的 feature code（服务器返回 error code 16572）",
                "27":"没有加密密钥（服务器返回 error code 16573）", "28":"物流数据无法读取"}
}



RemoteDownloadStatusUpdate = {
    "Status":{0:"Reserved", 1:"下载成功", 2:"下载失败"},
    "ECUID": {1:'IPK', 2:'FICM', 3:'TBOX', 4:'AC', 5:'PEPS', 6:'BCM', 7:'PMDC', 8:'GW', 9:'TCCM',
              10:'SDM', 11:'SCU', 12:'ECM', 13:'TCU', 14:'EPS', 15:'PDC', 16:'EPB', 17:'DHL', 18:'SCS',
              19:'ABS', 20:'SAS', 21:'FVCM', 22:'PLCM', 23:'HCU',  24:'BMS',  25:'TC',  26:'TPMS', 27:'APA',
              28:'ESCL', 29:'DCDC', 30:'VCU',  31:'ISC',  32:'OBC', 33:'ETC', 34:'FMU', 35:'GSMC', 36:'SAC',
              37:'EHBS', 38:'MSM', 39:'IECU', 40:'ALCM', 41:'FDR', 42:'RDA', 43:'P2P',44:'ibox'  },
    "FailReason": {0: "Reserved", 1: "成功，No reason", 2: "下载升级包失败",3: "升级包解密失败",3: "升级包解压失败",}
}

RemoteReflashStatusUpdate = {
    "Status": {0: "Reserved", 1: "刷新完成", 2: "刷新失败", 3:"刷新进行中", 4: "刷新开始"},
    "ECU_TYPE": {'00': 'Reserved', '01': 'to C', '02': 'to B'},
    "ECUID": {1:'IPK', 2:'FICM', 3:'TBOX', 4:'AC', 5:'PEPS', 6:'BCM', 7:'PMDC', 8:'GW', 9:'TCCM',
              10:'SDM', 11:'SCU', 12:'ECM', 13:'TCU', 14:'EPS', 15:'PDC', 16:'EPB', 17:'DHL', 18:'SCS',
              19:'ABS', 20:'SAS', 21:'FVCM', 22:'PLCM', 23:'HCU',  24:'BMS',  25:'TC',  26:'TPMS', 27:'APA',
              28:'ESCL', 29:'DCDC', 30:'VCU',  31:'ISC',  32:'OBC', 33:'ETC', 34:'FMU', 35:'GSMC', 36:'SAC',
              37:'EHBS', 38:'MSM', 39:'IECU', 40:'ALCM', 41:'FDR', 42:'RDA', 43:'P2P',44:'ibox' },

    "FailReason":{0:"Reserved", 1:"成功，No reason", 2:"HMI升级请求响应超时",
                  3:"升级条件不满足----未挂 P 档；（可进异常流程） ",
                  4:"升级条件不满足----电池电量不足以完成此次升级； （可进异常流程）",
                  5:"ECU升级失败（针对单个 ECU的状态更新）", 6:"升级条件不满足----发动机未关闭；（可进异常流 程）",
                  7:"正在检测更新", 8:"A1A4 解析错误", 9:"升级状态不满足（执行 APP 判断）",
                  10:"过防火墙失败", 11:"过安全访问失败",
                  12:"未升级完成（执行 APP 判断）", 13:"升级文件不完整或存在错误", 14:"TBOX MPU 升级失败",
                  15:"车速不满足条件", 16:"EPT 不满足条件", 17:"EPB 释放", 18:"PBS释放", 19:"Featurecode Error",
                  20:"ECU negative", 21:"TBOX PreConditionCheck 30s timeout", 22:"升级条件不满足----未充电",
                  23:"刷新单个 ECU 时电量不足", 24:"驻车电量不满足", 25:"BMS下电流程失败",26:"iBox MPU升级失败",
                  27:"iBox模组升级失败"
 }
}

AVNReflashModePermission = {
    'EnterPermission':{1:'不允许 AVN进入刷新模式',2:'允许 AVN进入刷新模式'}
}
RemoteReflashInform = {
    'ReflashReqInfo':{0:'Reserved', 1:'可选升级', 2:'强制升级'},
    'ECU_TYPE':{'00':'Reserved ','01':'to C', '02':'to B'}
}

RemoteReflashPerform = {
    'ApprovalResult':{0:'Reserved', 1:'立即执行', 2:'延后执行（预约升级）', 3:'暂不升级'},
    'ECUID':{1:'IPK', 2:'FICM', 3:'TBOX', 4:'AC', 5:'PEPS', 6:'BCM', 7:'PMDC', 8:'GW', 9:'TCCM',
              10:'SDM', 11:'SCU', 12:'ECM', 13:'TCU', 14:'EPS', 15:'PDC', 16:'EPB', 17:'DHL', 18:'SCS',
              19:'ABS', 20:'SAS', 21:'FVCM', 22:'PLCM', 23:'HCU',  24:'BMS',  25:'TC',  26:'TPMS', 27:'APA',
              28:'ESCL', 29:'DCDC', 30:'VCU',  31:'ISC',  32:'OBC', 33:'ETC', 34:'FMU', 35:'GSMC', 36:'SAC',
              37:'EHBS', 38:'MSM', 39:'IECU', 40:'ALCM', 41:'FDR', 42:'RDA', 43:'P2P',44:'ibox', 253:'（FD）：to B',
             254:'（FE）：to C',255:'（FF）：全部升级'}
}
RemoteReflashDetail = {
    'CHARGE_FLAG':{0:'需要', 1:'不需要'}
}

V2X_Function_Status = {
    1:{'v2x开关':'关闭','智能ACC开关':''},
    2:{'v2x开关':'开关打开无运行','智能ACC开关':'关闭'},
    3:{'v2x开关':'开关打开在运行','智能ACC开关':'关闭'},
    4:{'v2x开关':'开关打开无运行','智能ACC开关':'开关打开无运行'},
    5:{'v2x开关':'开关打开在运行','智能ACC开关':'开关打开无运行'},
    6:{'v2x开关':'开关打开在运行','智能ACC开关':'开关打开在运行'},
}

RoadInformation = {
    'RoadInfo03':{
                0:"无标识",
                1:"向左急转弯",
                2:"向右急转弯",
                3:"左侧绕行",
                4:"右侧绕行",
                5:"左右绕行",
                6:"反向弯路",
                7:"连续弯路"
    },
    'RoadInfo05':{
            0:"无标识",
            1:"慢行",
            2:"减速让行"
    },
    'RoadInfo09': {
        0:"无标识",
        1:"注意行人",
        2:"注意儿童",
        3:"注意牲畜",
        4:"注意落石（左边）",
        5:"注意落石（右边）",
        6:"傍山险路（左边）",
        7:"傍山险路（右边）",
        8:"堤坝路（左边）",
        9:"堤坝路（右边）",
        10:"渡口",
        11:"两侧变窄",
    }
}