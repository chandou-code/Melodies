# -*- coding: utf-8 -*-
from pydub.silence import detect_silence

import Toolbox
import Current_lry
from pydub import AudioSegment
from pydub.silence import detect_silence
import difflib


def convert_time_to_milliseconds(time_str):
    """将时间字符串转换为毫秒"""
    minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split('.')
    return int(minutes) * 60 * 1000 + int(seconds) * 1000 + int(milliseconds)


def convert_milliseconds_to_time(ms):
    """将毫秒转换为时间字符串"""
    milliseconds = ms % 1000
    total_seconds = ms // 1000
    seconds = total_seconds % 60
    minutes = total_seconds // 60

    return f"{minutes:02}:{seconds:02}.{milliseconds:03}"
def process_audio(segment,audio):

    start_time = convert_time_to_milliseconds(segment['start'])
    end_time = convert_time_to_milliseconds(segment['end'])

    # 切割音频

    # 检测静音
    silence_start = end_time
    silence_end = min(end_time + 1000, len(audio))  # 向后1秒内查找静音
    silences_end = detect_silence(audio[silence_start:silence_end], min_silence_len=200, silence_thresh=-20)


    silence_start_check = max(0, start_time - 100)  # 向前1秒内查找静音
    silence_end_check = min(start_time + 1000, len(audio))  # 向后1秒内查找静音
    silences_start = detect_silence(audio[silence_start_check:silence_end_check], min_silence_len=150,
                                    silence_thresh=-20)


    if silences_end:
        # 找到第一个静音部分
        true_end_time = end_time + silences_end[-1][0]  # 获取静音起始时间

    else:
        true_end_time = end_time  # 如果没有静音，则保持原来的结束时间

    if silences_start:
        # 找到第一个静音部分
        true_start_time = start_time

        true_start_time = start_time + silences_start[0][1]  # 获取静音起始时间
        # print('silences_start',silences_start,'start_time',start_time,'silence_start + silences_start[0][1]',start_time + silences_start[0][1])
    else:
        true_start_time = start_time  # 如果没有静音，则保持原来的结束时间
    # print(f"true_start_time", true_start_time, " true_end_time", true_end_time)
    audio_segment = audio[true_start_time:true_end_time]
    # 保存切割后的音频
    # print(f"OK_1.wav")
    true_start_time=convert_milliseconds_to_time(true_start_time)
    true_end_time=convert_milliseconds_to_time(true_end_time)
    return audio_segment,true_start_time,true_end_time


def main_main(url, file):
    # url='https://music.163.com/song?id=1878812258&userid=129707286'
    eng, cn = Toolbox.download_lyr(Toolbox.get_id(url))
    tt = Current_lry.LRY().lry(eng, cn)
    tt = handle_tt_second(tt, file)
    print('分割之后', tt)
    return tt


def handle_tt_second(tt, file):

    index = 0
    audio = AudioSegment.from_file(file)

    for t in tt:
        if t['start'] and t['end'] and t['text'] and t['cntext']:

            audio_segment,start,end = process_audio(t,audio)
            t['start']=start
            t['end']=end
            output = f"temp/OK_{index}.wav"
            audio_segment.export(output, format="wav")
            tt[index]['path'] = output
            index += 1
        else:
            index += 1

    filtered_tt = []
    for t in tt:
        if t['start'] and t['end'] and t['text'] and t['cntext']:
            start = t['start']
            end = t['end']
            start_ms = convert_time_to_milliseconds(start)
            end_ms = convert_time_to_milliseconds(end)
            if end_ms - start_ms >= 1000:  # 保留时间差大于等于 1000 毫秒的元素
                filtered_tt.append(t)

    tt = filtered_tt  # 更新 tt 为过滤后的结果
    tt = [t for t in tt if 'path' in t]
    tt = remove_similar(tt)
    print('endtt', tt)
    return tt


def get_right_lry(text1, text2):
    similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    return float(f'{similarity:.2f}')


def remove_similar(tt, threshold=0.9):
    unique_entries = []  # 存储唯一的条目

    for entry in tt:
        text = entry['text']
        is_similar = False

        for unique_entry in unique_entries:
            if get_right_lry(text, unique_entry['text']) > threshold:
                is_similar = True
                break  # 如果找到相似度大于阈值的句子，则停止检查

        if not is_similar:
            unique_entries.append(entry)  # 如果没有相似句子，则添加到列表

    return unique_entries


if __name__ == '__main__':
    url = 'https://music.163.com/song?id=531672176&userid=1400200533'
    eng, cn = Toolbox.download_lyr(Toolbox.get_id(url))
    tt = Current_lry.LRY().lry(eng, cn)

    temp = tt[0]
    print(temp)
    audio_segment = process_audio('music/Kailee Morgue - Unfortunate Soul_noreverb.mp3', temp)
    output = f"temp/OK_111.wav"
    audio_segment.export(output, format="wav")
    # process_audio()
    # main(url)
