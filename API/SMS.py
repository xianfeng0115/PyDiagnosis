#coding:utf-8

import random
import AcsClient
import region_provider

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"
SIGN_NAME = '你的签名'   # 可以设置多个，按需求选取即可

# ACCESS_KEY_ID 和 ACCESS_KEY_SECRET 为阿里云短信申请的
ACCESS_KEY_ID = ""
ACCESS_KEY_SECRET = ""
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

def ali_send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    sms_request = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    sms_request.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        sms_request.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    sms_request.set_OutId(business_id)

    # 短信签名
    sms_request.set_SignName(sign_name)

    # 短信发送的号码列表，必填。
    sms_request.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    sms_response = acs_client.do_action_with_exception(sms_request)
    sms_rsp = json.loads(sms_response)
    if sms_rsp.get('Code') != 'OK':
        log.exception('========短信发送失败 原因')
        log.exception(sms_rsp.get('Message')+'，'+str(phone_numbers))
        return False
    return True

def send_sms(mobile_no, content, template_code):
    """
    发送短信
    :param mobile_no: 手机号码
    :param content: 发送内容（json格式）
    :param template_code: 模板代码
    :return:
    """
    try:
        __business_id = uuid.uuid1()
        params = content
        send_res = ali_send_sms(__business_id, mobile_no, SIGN_NAME, template_code, params)
        return send_res

    except Exception as ex:
        log.exception(ex)
        return False



def send_verify_code(mobile_no, template_code, random_number=None):
    """
    发送校验码
    :param mobile_no: 手机号码
    :param random_number: 验证码
    :param template_code: 模板代码
    :return:
    """
    if random_number is None:
        random_number = random.randrange(1, 10000, 5)
    content = '{"code": "' + str(random_number) + '"}'
    return send_sms(mobile_no, content, template_code)

if __name__ == '__main__':
    # 发送验证码
    send_verify_code("要发送的电话号码",  "你申请的验证码模板CODE")
    # 发送通知短信
    content = dict()
    content['name'] = '帅帅的吾延'   # name 为你申请短信模板的参数
    content['content'] = '吾延是真的帅'  # content为你申请短信模板的参数
    send_sms("要发送的电话号码", content,  "你申请的验证码模板CODE")