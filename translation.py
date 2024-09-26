import hashlib
import os
import time

import requests
import random
import urllib.parse
import json
import http.client


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


class baiduTranslate_F:
    def baiduTranslate(self, translate_text):
        print('translate_text',translate_text)
        text = None
        while text is None:
            time.sleep(1)
            text = baiduTranslate().baiduTranslate(translate_text, 0)
        # text = '百度翻译已完成'
        print(f'{text}|百度翻译已完成')
        return text

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
