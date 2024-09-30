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
    def lry(self, input_string, input_cn_string):

        if any(line.startswith("[by:") for line in input_string.splitlines()):
            # 如果有以 [by: 开头的行，使用第一种模式
            pattern = r'\[(\d{2}:\d{2}\.\d{2})\](.*?)(?=\[\d{2}:\d{2}\.\d{2}\]|$)'
            input_string = "\n".join([line for line in input_string.splitlines() if not line.startswith("[by:")])
            input_cn_string = "\n".join([line for line in input_cn_string.splitlines() if not line.startswith("[by:")])
        else:
            # 否则使用第二种模式
            pattern = r'\[(\d{2}:\d{2}\.\d{3})\](.*?)(?=\[\d{2}:\d{2}\.\d{3}\]|$)'


        # print('input_string',input_string)
        # print('input_cn_string',input_cn_string)
        # 使用正则表达式匹配时间戳和文本

        # pattern = r'\[(\d{2}:\d{2}\.\d{2})\](.*?)(?=\[\d{2}:\d{2}\.\d{2}\]|$)'
        # pattern = r'\[(\d{2}:\d{2}\.\d{3})\](.*?)(?=\[\d{2}:\d{2}\.\d{3}\]|$)'


        matches1 = re.findall(pattern, input_string, re.DOTALL)
        matches2 = re.findall(pattern, input_cn_string, re.DOTALL)
        # print('matches1', matches1)
        # print('matches2', matches2)
        # 转换为字典列表
        result1 = []
        for i, (start, text) in enumerate(matches1):
            end = matches1[i + 1][0] if i + 1 < len(matches1) else None

            # 找到对应的中文文本
            cn_text = matches2[i][1].strip() if i < len(matches2) else None

            result1.append({'text': text.strip(), 'start': start, 'end': end, 'cntext': cn_text})

        return result1

    def get_right_lry(self, text1, text2):
        similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
        # print(f"相似度: {similarity:.2f}")
        return float(f'{similarity:.2f}')

    def score(self, transcribed_text, texts):
        index = 0
        print(texts)
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

        if highest_index + 1 < len(texts):  # 确保索引不越界
            text += f" {texts[highest_index + 1]['text']}"
            cntext += f" {texts[highest_index + 1]['cntext']}"
            # print('\n')
            # print(text)
            # print(cntext)
        score = self.get_right_lry(transcribed_text, text)
        if score > 0.8:
            # print('best_match_text', '|', transcribed_text, cntext)
            return text, cntext, score
        else:
            cntext = translation.baiduTranslate_F().baiduTranslate(transcribed_text)
            return transcribed_text, cntext, 0


class LRYf():
    def lryF(self, url, tk):
        eng, cn = Toolbox.download_lyr(Toolbox.get_id(url))

        l = LRY()
        transcribed_text = tk['text']
        texts = l.lry(eng, cn)
        print('texts', texts)
        text, cntext, score = l.score(transcribed_text, texts)
        logging.info(f'{text}|{cntext}|{score}')
        # print(text, cntext, score)
        return text, cntext


# if __name__ == '__main__':
#     # input_string = '[00:02.366]Lately I wanna stay awake\n[00:04.866]I don’t want the days to end\n[00:09.866]I know you’ll fly away\n[00:12.615]Need to hold you for myself\n[00:17.115]I feel the time run through my hands\n[00:20.115]Try to grab it but it fades\n[00:23.120]Say "goodbye" in all the possible ways\n[00:31.619]I don’t want you to get lost\n[00:34.117]Will we ever meet again?\n[00:35.869]I’ll anesthetize the pain\n[00:37.617]Please remember our summers\n[00:39.620]My heart is closed by duel\n[00:41.620]Will I learn to love again?\n[00:43.616]Who will walk with me in the rain?\n[00:45.618]Please remember our summers\n[01:18.116]Come the sun,\n[01:20.116]come the rain\n[01:22.616]and the leaves falling\n[01:25.616]I will wait even if the seasons change\n[01:31.918]Anxiety runs through my veins\n[01:35.069]I’ll escape from all these chains\n[01:37.869]Say “come back”, in all the possible ways\n[01:46.367]I don’t want you to get lost\n[01:48.867]Will we ever meet again?\n[01:50.867]I’ll anesthetize the pain\n[01:52.867]Please remember our summers\n[01:54.620]My heart is closed by duel\n[01:56.617]Will I learn to love again?\n[01:58.367]Who will walk with me in the rain?\n[02:00.367]Please remember our summers'
#     # input_cn_string='[00:02.366]最近我想保持清醒\n[00:04.866]我舍不得这些美好的日子就这样结束\n[00:09.866]我明白你终究会离我远去\n[00:12.615]我多想紧紧抱住你留住你的一丝气息\n[00:17.115]我能感受得到时光如沙，在我掌心里慢慢流逝\n[00:20.115]我疯狂地想紧紧抓住，但它只是流逝得更快\n[00:23.120]用任何可能的方式说再见\n[00:31.619]我不想把你弄丢\n[00:34.117]我们还会再见面吗？\n[00:35.869]我会麻醉疼痛自己疗伤\n[00:37.617]请你记住我们一起度过的那些夏天\n[00:39.620]我的心门被紧紧关闭了\n[00:41.620]我还能再次拥有爱一个人的能力吗？\n[00:43.616]谁还会再陪我在雨中漫步？\n[00:45.618]请你，一定要记得我们一起度过的那些夏天\n[01:18.116]在阳光下\n[01:20.116]在雨中\n[01:22.616]在落叶纷飞里\n[01:25.616]四季交替，我会一直在这里等你\n[01:31.918]悲伤与焦虑顺着血管在我身体里蔓延\n[01:35.069]我终有一天能挣脱这些痛苦的枷锁\n[01:37.869]说“回来吧”，用所有可能的方式\n[01:46.367]我不想把你弄丢\n[01:48.867]我们还会再见面吗？\n[01:50.867]我会麻醉疼痛自己疗伤\n[01:52.867]请你记住我们一起度过的那些夏天\n[01:54.620]我的心门被紧紧关闭了\n[01:56.617]我还能再次拥有爱一个人的能力吗？\n[01:58.367]谁还会再陪我在雨中漫步？\n[02:00.367]请你一定要记得我们一起度过的那些夏天'
#     # file='temp/OK_0.wav'
#     tks = [{'path': 'temp\\OK_0.wav',
#             'text': "I threw a wish in the well, don't ask me I'll never tell, I looked at you as it fell"},
#            {'path': 'temp\\OK_1.wav', 'text': "And now you're in my way"},
#            {'path': 'temp\\OK_2.wav', 'text': 'I trade my soul for a wish'}]
#
#     url = 'https://music.163.com/song?id=17112299&userid=129707286'
#
#     print(LRYf().lryF(url, tks[2]))
