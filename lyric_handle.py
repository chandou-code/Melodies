import os
import re
import shutil
import requests


class lyric1():
    def get_time(self, matches):
        # 使用正则表达式提取时间戳和文本
        timestamps = []
        texts = []
        for matche in matches:
            match = re.match(r'\[(.*?)\](.*)', matche)
            if match:
                timestamps.append(match.group(1))  # 添加时间戳
                texts.append(match.group(2))  # 添加文本并去除多余空格
        # 删除包含括号的元素

        return timestamps, texts

    def get_lyr(self, lyric):
        # print(lyr)
        pattern = r'(\[.*?\].*?)(?=\n|\Z)'
        matches = re.findall(pattern, lyric.strip())
        # matches = [matche for matche in matches if len(matche.split(' ')[0]) != 11]  # 过滤列表

        matches = [item for item in matches if item.count(':') < 2]
        # print(matches)

        return matches

    def get_Tick(self, t):
        minutes, seconds = t.split(':')
        Tick = int(float(int(minutes) * 60 + float(seconds)) * 1000)
        return Tick

    def get_tks(self, timestamps, texts):
        index = 0

        tks = []
        while index < len(timestamps):
            word_count = len(texts[index].split())
            # print(texts[index])

            if texts[index] != '':
                if index + 1 < len(timestamps) and word_count <= 5 and index + 2 < len(timestamps):
                    tk = {
                        'text': f'{texts[index]} {texts[index + 1]}',
                        'begin': timestamps[index],
                        'end': timestamps[index + 2]
                    }

                    tks.append(tk)
                    index += 2  # Move forward by 2 since we combined two texts
                else:
                    tk = {

                        'text': texts[index],
                        'begin': timestamps[index],
                        'end': timestamps[index + 1]
                        # Ensure we don't go out of bounds

                    }
                    tks.append(tk)
                    index += 1  # Move forward by 1

            elif texts[index] == '':
                index += 1  # Move forward to skip empty text

            # Add a safety condition to break in case of unexpected infinite loop
            if index >= len(timestamps):
                break
        return tks


class lyricF():
    def lyricF(self,lyric):

        # lyric="[00:00.130]Lately, I've been, I've been losing sleep\n[00:04.990]Dreaming about the things that we could be\n[00:09.030]But baby, I've been, I've been praying hard,\n[00:13.320]Said no more counting dollars\n[00:15.870]We'll be counting stars, yeah we'll be counting stars\n[00:24.630]\n[00:37.580]I see this life like a swinging vine\n[00:40.160]Swing my heart across the line\n[00:41.990]And my face is flashing signs\n[00:44.300]Seek it out and you shall find\n[00:46.120]Old, but I'm not that old\n[00:48.170]Young, but I'm not that bold\n[00:50.000]I don't think the world is sold\n[00:51.760]On just doing what we're told\n[00:54.250]I~ feel something so right\n[00:58.720]Doing the wrong thing\n[01:01.710]I~ feel something so wrong\n[01:06.470]Doing the right thing\n[01:10.060]I could lie, could lie, could lie\n[01:13.050]Everything that kills me makes me feel alive\n[01:17.730]\n[01:17.950]Lately, I've been, I've been losing sleep\n[01:21.460]Dreaming about the things that we could be\n[01:25.450]But baby, I've been, I've been praying hard,\n[01:29.300]Said, no more counting dollars\n[01:31.450]We'll be counting stars\n[01:32.950]\n[01:33.290]Lately, I've been, I've been losing sleep\n[01:37.080]Dreaming about the things that we could be\n[01:40.770]But baby, I've been, I've been praying hard,\n[01:44.960]Said, no more counting dollars\n[01:47.140]We'll be, we'll be counting stars\n[01:50.290]\n[01:56.290]I feel the love and I feel it burn\n[01:58.710]Down this river, every turn\n[02:00.710]Hope is our four-letter word\n[02:02.620]Make that money, watch it burn\n[02:04.870]Old，but I'm not that old\n[02:06.750]Young, but I'm not that bold\n[02:08.720]I don't think the world is sold\n[02:10.990]On just doing what we're told\n[02:12.770]I~ feel something so wrong\n[02:17.250]By Doing the right thing\n[02:20.680]I could lie, could lie, could lie\n[02:24.470]Everything that drowns me makes me wanna fly\n[02:28.540]\n[02:28.790]Lately, I've been, I've been losing sleep\n[02:32.180]Dreaming about the things that we could be\n[02:35.930]But baby, I've been, I've been praying hard,\n[02:40.030]Said  no more counting dollars\n[02:42.310]We'll be counting stars\n[02:43.810]\n[02:44.030]Lately, I've been, I've been losing sleep\n[02:47.800]Dreaming about the things that we could be\n[02:51.600]But baby, I've been, I've been praying hard,\n[02:56.000]Said, no more counting dollars\n[02:58.040]We'll be, we'll be counting stars\n[03:00.840]\n[03:04.120]Take that money\n[03:04.630]Watch it burn\n[03:05.630]Sink in the river\n[03:06.710]The lessons I've learned\n[03:07.440]\n[03:07.730]Take that money\n[03:08.320]Watch it burn\n[03:09.440]Sink in the river\n[03:10.550]The lessons I've learned\n[03:11.380]\n[03:11.660]Take that money\n[03:12.610]Watch it burn\n[03:13.520]Sink in the river\n[03:14.430]The lessons I've learned\n[03:15.320]\n[03:15.600]Take that money\n[03:16.610]Watch it burn\n[03:17.480]Sink in the river\n[03:18.450]The lessons I've learned\n[03:19.160]\n[03:19.500]Everything that kills me makes me feel alive\n[03:26.700]\n[03:26.790]Lately, I've been, I've been losing sleep\n[03:30.150]Dreaming about the things that we could be\n[03:33.890]But baby, I've been, I've been praying hard,\n[03:38.170]Said, no more counting dollars\n[03:40.190]We'll be counting stars\n[03:41.610]\n[03:41.910]Lately, I've been, I've been losing sleep\n[03:45.520]Dreaming about the things that we could be\n[03:49.720]But baby, I've been, I've been praying hard,\n[03:53.900]Said, no more counting dollars\n[03:55.980]We'll be, we'll be, counting stars\n[03:57.910]\n[03:58.090]Take that money\n[03:58.860]Watch it burn\n[03:59.750]Sink in the river\n[04:00.740]The lessons I've learned\n[04:01.440]\n[04:01.840]Take that money\n[04:02.790]Watch it burn\n[04:03.770]Sink in the river\n[04:04.680]The lessons I've learned\n[04:05.430]\n[04:05.790]Take that money\n[04:06.750]Watch it burn\n[04:07.620]Sink in the river\n[04:08.520]The lessons I've learned\n[04:09.290]\n[04:09.660]Take that money\n[04:10.700]Watch it burn\n[04:11.690]Sink in the river\n[04:12.610]The lessons I've learned\n[04:13.690]"
        l = lyric1()
        lyric = l.get_lyr(lyric)
        print(lyric)
        timestamps, texts = l.get_time(lyric)

        # 获取最后一个时间戳并增加三秒
        last_timestamp = timestamps[-1]
        minutes, seconds = map(float, last_timestamp.split(':'))
        new_seconds = seconds + 3

        # 如果秒数超过60，进行转换
        if new_seconds >= 60:
            minutes += int(new_seconds // 60)
            new_seconds %= 60

        # 格式化时间戳，确保分钟和秒数都有前导零
        new_timestamp = f"{int(minutes):02}:{new_seconds:06.3f}"

        # 插入新元素
        timestamps.append(new_timestamp)
        texts.append('')

        # for text in texts:
        #     print(text)
        tks = l.get_tks(timestamps, texts)
        #

        # 删除包含括号的元素
        tks = [item for item in tks if '(' not in item['text'] and ')' not in item['text']]
        tks = [item for item in tks if not item['text'].startswith(' ')]
        print(tks)


        # for i in range(len(tks) - 1, -1, -1):
        #     if l.get_Tick(tks[i]['end']) - l.get_Tick(tks[i]['begin']) > 15000:
        #         # print(tks[i]['text'])
        #         del tks[i]  # 删除满足条件的元素

        return tks
