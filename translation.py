import hashlib
import os
import time

import requests
import random
import urllib.parse
import json
import http.client
import requests
import time
import random
from hashlib import md5


class baiduTranslate():
    def baiduTranslate(self, translate_text, flag=1):

        appid = '20240918002153723'  # 填写你的appid
        secretKey = 'tJl1tcva0eOwrD_HPQJJ'  # 填写你的密钥
        httpClient = None
        myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址
        fromLang = 'auto'  # 原文语种

        if flag:
            toLang = 'en'  # 译文语种
        else:
            toLang = 'zh'  # 译文语种

        salt = random.randint(3276, 65536)

        sign = appid + translate_text + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(translate_text) + '&from=' + fromLang + \
                '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

        # 建立会话，返回结果
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)

            # return result
            return result['trans_result'][0]['dst']

        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()

    def youdaoTranslate(self, text):

        headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-690213934@10.108.162.139; OUTFOX_SEARCH_USER_ID_NCOO=1273672853.5782404; fanyi-ad-id=308216; fanyi-ad-closed=1; ___rl__test__cookies=1659506664755',
            'Host': 'fanyi.youdao.com',
            'Origin': 'https://fanyi.youdao.com',
            'Referer': 'https://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        key = text
        lts = str(int(time.time() * 100))
        salt = lts + str(random.randint(0, 9))
        sign_data = 'fanyideskweb' + key + salt + 'Ygy_4c=r#e#4EX^NUGUc5'
        sign = md5(sign_data.encode()).hexdigest()
        data = {
            'i': key,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            # 时间戳  1970  秒
            'salt': salt,
            # 加密
            'sign': sign,
            # 时间戳
            'lts': lts,
            # 加密的数据
            'bv': 'f0819a82107e6150005e75ef5fddcc3b',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }

        # 获取到资源地址
        url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        response = requests.post(url, headers=headers, data=data)

        tgt_value = response.json()["translateResult"][0][0]["tgt"]
        return tgt_value


class baiduTranslate_F:
    def Translate(self, translate_text):
        # print('translate_text', translate_text)
        text = None
        while text is None:
            time.sleep(1)
            text = baiduTranslate().youdaoTranslate(translate_text)
        # text = '百度翻译已完成'
        print(f'{text}|有道翻译已完成')
        return text
    # def Translate(self, translate_text):
    #     print('translate_text',translate_text)
    #     text = None
    #     while text is None:
    #         time.sleep(1)
    #         text = baiduTranslate().baiduTranslate(translate_text, 0)
    #     # text = '百度翻译已完成'
    #     print(f'{text}|百度翻译已完成')
    #     # return text

# def main():
#
#
#     # 输入需要翻译的文本
#     translate_text = "hello,world "
#
#     # 调用翻译方法
#     translated_text = baiduTranslate_F().baiduTranslate(translate_text)
#
#     # 打印翻译结果
#     print(f"翻译结果: {translated_text}")
#
#
# if __name__ == "__main__":
#     main()
