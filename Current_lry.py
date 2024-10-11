# -*- coding: utf-8 -*-
import re
import whisperwhisper
import difflib
import Toolbox
from myproject.musics import translation
import logging

# 配置日志设置
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# 输入字符串
class LRY():
    def remove_parentheses_content(self,input_string):
        # 使用正则表达式匹配括号及其中的内容
        result = re.sub(r'\(.*?\)', '', input_string)
        return result.strip()  # 去掉前后的空白
    def lry(self, input_string, input_cn_string):
        input_cn_string=self.remove_parentheses_content(input_cn_string)
        input_string = input_string.replace('\u2005', '').replace('\xa0',' ')
        # print(repr(input_string))
        if self.check_mode(input_string) == 4 or self.check_mode(input_cn_string) == 4:
            pattern = r'\[(\d{2}:\d{2}\.\d{3})\](.*?)(?=\[\d{2}:\d{2}\.\d{3}\]|$)'

            input_string = "\n".join([line for line in input_string.splitlines() if not line.startswith("[by:")])
            input_cn_string = "\n".join([line for line in input_cn_string.splitlines() if not line.startswith("[by:")])
        else:
            # 否则使用第二种模式
            pattern = r'\[(\d{2}:\d{2}\.\d{2})\](.*?)(?=\[\d{2}:\d{2}\.\d{2}\]|$)'


        matches1 = re.findall(pattern, input_string, re.DOTALL)
        matches2 = re.findall(pattern, input_cn_string, re.DOTALL)
        # print(matches1)
        # print(matches2)
        # 转换为字典列表
        result1 = []
        for i, (start, text) in enumerate(matches1):
            end = matches1[i + 1][0] if i + 1 < len(matches1) else None

            if text.strip():  # 检查 text 是否为空
                result1.append({'text': text.strip(), 'start': start, 'end': end})

        result2 = []
        for i, (start, text) in enumerate(matches2):
            end = matches2[i + 1][0] if i + 1 < len(matches2) else None

            if text.strip():  # 检查 text 是否为空
                result2.append({'cntext': text.strip(), 'start': start, 'end': end})
        combined_results = {}

        # 将 result1 的数据存入字典
        for entry in result1:
            start = entry['start']
            combined_results[start] = {
                'text': entry['text'],
                'end': entry['end'],
                'cntext': None  # 初始化 cntext 为 None
            }

        # 将 result2 的数据合并到字典中
        for entry in result2:
            start = entry['start']
            if start in combined_results:
                combined_results[start]['cntext'] = entry['cntext']  # 更新 cntext

        # 将字典转换为列表
        final_result = [{'start': start, **data} for start, data in combined_results.items()]


        return final_result

    def check_mode(self, input_string):

        start_index = input_string.find('[00')
        if start_index != -1:
            # 切片，从 '[00' 开始到字符串结束
            input_string = input_string[start_index:]
            # print(repr(input_string))

        start_index = input_string.find('[')
        end_index = input_string.find(']', start_index)

        # 提取并打印第一个时间戳
        if start_index != -1 and end_index != -1:
            first_timestamp = input_string[start_index:end_index + 1]
            return len(first_timestamp.split('.')[-1])

    def get_right_lry(self, text1, text2):
        similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
        # print(f"相似度: {similarity:.2f}")
        return float(f'{similarity:.2f}')

    def score(self, transcribed_text, texts):
        index = 0
        # print(texts)
        highest_score = 0
        highest_index = 0

        while index < len(texts):
            highest_index = 0
            text = texts[index]['text']
            cntext = texts[index]['cntext']
            score = self.get_right_lry(transcribed_text, text)

            if score > highest_score:  # 获取最高分highest_score 对应的英文文本best_match_text 和下标highest_index
                highest_score = score

                highest_index = index

            if score > 0.8:  # 情况1恰好匹配上 只有几个字不同 返回歌词部分
                # print('Translation found:', transcribed_text, '|', text)
                return text, cntext, score

            # print('No translation:', transcribed_text, '|', text)

            index += 1

        # if best_match_text is not None:  # 如果没匹配上就用匹配度最高的那句向后融合一段 再次匹配 如果依旧没法匹配就返回原来的东西 并且百度翻译
        # print('Highest score:', highest_score, 'Best match text:', best_match_text, highest_index)
        #     pass
        # print('highest_index', highest_index)

        text = texts[highest_index]['text']
        cntext = texts[highest_index]['cntext']

        # if highest_index + 1 < len(texts):  # 确保索引不越界
        #     text += f" {texts[highest_index + 1]['text']}"
        #     cntext += f" {texts[highest_index + 1]['cntext']}"
        # print('\n')
        # print(text)
        # print(cntext)
        score = self.get_right_lry(transcribed_text, text)
        if score > 0.8:
            # print('best_match_text', '|', transcribed_text, cntext)
            return text, cntext, score
        else:
            cntext = translation.baiduTranslate_F().Translate(transcribed_text)
            return transcribed_text, cntext, 0


class LRYf():
    def lryF(self, url, tk):
        eng, cn = Toolbox.download_lyr(Toolbox.get_id(url))

        transcribed_text = tk['text']
        texts = LRY().lry(eng, cn)

        text, cntext, score = LRY().score(transcribed_text, texts)
        # logging.info(f'{text}|{cntext}|{score}')
        # print(text, cntext, score)
        return text, cntext

if __name__ == '__main__':
    matches1=[('00:16.103', ' How many times can I tell you\n'), ('00:20.331', " You're lovely just the way you are\n"), ('00:24.140', " Don't let the world come and change you\n"), ('00:28.685', " Don't let life break your heart\n"), ('00:31.884', " Don't put on their mask don't wear their disguise\n"), ('00:35.503', " Don't let them dim the light that shines in your eyes\n"), ('00:39.566', ' If only you could love yourself the way that I love you\n'), ('00:47.154', '\n'), ('01:03.063', ' How many times can I say\n'), ('01:07.696', " You don't have to change a thing\n"), ('01:10.776', " Don't let the tide wash you away\n"), ('01:15.482', " Don't let worry ever clip your wings\n"), ('01:19.140', ' Discard what is fake keep what is real\n'), ('01:22.897', ' Pursue what you love embrace how you feel\n'), ('01:26.634', ' If only you could love yourself the way that I love you\n'), ('01:34.842', '\n'), ('01:39.066', ' And if you ever choose a road that leads nowhere\n'), ('01:45.225', " All alone and you can't see right from wrong\n"), ('01:54.944', ' And if you ever lose yourself out there\n'), ('02:01.528', ' Come on home\n'), ('02:03.933', " And I'll sing you this song\n"), ('02:06.993', '\n'), ('02:10.722', ' So how many times can I tell you\n'), ('02:16.362', " You're lovely just the way you are\n"), ('02:19.461', " Don't let the world come and change you\n"), ('02:24.554', " Don't let life break your heart")]
    matches2=[('00:16.103', '我已无数次地告诉过你\n'), ('00:20.331', '你本就是你那副纯粹可爱的模样\n'), ('00:24.140', '请不要任由世界将你所改变\n'), ('00:28.685', '也别让生活令你心碎至极\n'), ('00:31.884', '不要戴上虚伪的面具 将自己伪装\n'), ('00:35.503', '也别任由他人 黯淡你眼中的光芒\n'), ('00:39.566', '倘若你能像我爱你这样 爱自己 那该多好\n'), ('01:03.063', '我早就说过无数次了\n'), ('01:07.696', '你无需做出改变\n'), ('01:10.776', '不要任由洪荒将你本貌所涤荡\n'), ('01:15.482', '也别让愁苦忧虑 将你的羽翼禁锢\n'), ('01:19.140', '摒弃虚伪 保持真我\n'), ('01:22.897', '竭力追寻心之所向 拥抱心扉所感\n'), ('01:26.634', '倘若你能像我爱你这样 爱自己 那该多好\n'), ('01:39.066', '倘若你误入歧途 不得出逃\n'), ('01:45.225', '孤零飘荡 无法辨识正确去向\n'), ('01:54.944', '倘若你就此迷失真我\n'), ('02:01.528', '那便 返璞归真吧\n'), ('02:03.933', '我将为你吟唱这首歌谣\n'), ('02:10.722', '我已无数次地告诉过你\n'), ('02:16.362', '你本就是你那副纯粹可爱的模样\n'), ('02:19.461', '请不要任由世界将你所改变\n'), ('02:24.554', '也别让生活令你心碎至极')]
    print(matches1)
    print(matches2)
