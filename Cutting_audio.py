# -*- coding: utf-8 -*-
import time

from pydub.silence import detect_silence

import Toolbox
import Current_lry
from pydub import AudioSegment
from pydub.silence import detect_silence
import difflib

from pydub import AudioSegment

import librosa.display

from scipy.signal import butter, filtfilt
from scipy.ndimage import gaussian_filter

import librosa
import librosa.display

import numpy as np
import librosa
import matplotlib.pyplot as plt






def process_audio(segment, audio):
    start_time = convert_time_to_milliseconds(segment['start'])
    end_time = convert_time_to_milliseconds(segment['end'])

    # 切割音频

    # 检测静音
    silence_start = end_time - 1000  # 向前1秒内查找静音
    silence_end = min(end_time + 1000, len(audio))  # 向后1秒内查找静音
    silences_end = detect_silence(audio[silence_start:silence_end], silence_thresh=-40)

    silence_start_check = max(0, start_time - 100)  # 向前1秒内查找静音
    silence_end_check = min(start_time + 200, len(audio))  # 向后1秒内查找静音
    silences_start = detect_silence(audio[silence_start_check:silence_end_check],
                                    silence_thresh=-40)
    print('silences_end', silences_end)
    if silences_end:
        # 找到第一个静音部分
        true_end_time = end_time + silences_end[-1][0]  # 获取静音起始时间
        # nearest_silence_start = min(silences_end, key=lambda x: abs(end_time - x[0]))  # 找到与end_time最近的静音
        # true_end_time = end_time + nearest_silence_start[0]  # 获取最近的静音起始时间

    else:
        true_end_time = end_time  # 如果没有静音，则保持原来的结束时间
    # true_end_time = end_time
    print('silences_start', silences_start)
    if silences_start:
        # 初始化 true_start_time
        # true_start_time = start_time
        true_start_time = start_time + silences_start[0][1]  # 获取静音起始时间
        # 找到距离最近的静音部分
        # nearest_silence = min(silences_start, key=lambda silence: abs((start_time + silence[1]) - start_time))

        # true_start_time = start_time + nearest_silence[1]  # 获取最近静音的起始时间
        # print('silences_start', silences_start, 'start_time', start_time, 'nearest_silence', nearest_silence)

    else:
        true_start_time = start_time  # 如果没有静音，则保持原来的结束时间
    # true_start_time=start_time
    # print(f"true_start_time", true_start_time, " true_end_time", true_end_time)

    # audio_segment = audio_with_sound[true_start_time:true_end_time]
    # 保存切割后的音频
    # print(f"OK_1.wav")
    true_start_time_ms = true_start_time
    true_end_time_ms = true_end_time
    true_start_time = convert_milliseconds_to_time(true_start_time)
    true_end_time = convert_milliseconds_to_time(true_end_time)
    return true_start_time, true_end_time, true_start_time_ms, true_end_time_ms


def handle_tt_second(tt, file):
    index = 0
    audio = AudioSegment.from_file(file)
    file = file.split('_')[0] + '.mp3'
    audio_with_sound = AudioSegment.from_file(file)
    tt = [tt[0]]
    print('tt1', tt)
    for t in tt:
        if t['start'] and t['end'] and t['text'] and t['cntext']:
            start, end, true_start_time_ms, true_end_time_ms = process_audio(t, audio)
            t['start'] = start
            t['end'] = end
            audio_segment = audio[true_start_time_ms:true_end_time_ms]
            audio_segment_sound = audio_with_sound[true_start_time_ms:true_end_time_ms]
            output1 = f"temp/OK1_{index}_{time.time()}.wav"
            output2 = f"temp/OK2_{index}_{time.time()}.wav"
            audio_segment.export(output1, format="wav")
            audio_segment_sound.export(output2, format="wav")
            tt[index]['path'] = output1
            tt[index]['sound_path'] = output2
            index += 1
        else:
            index += 1

    filtered_tt = []
    for i in range(len(tt)):
        if all(key in tt[i] for key in ['start', 'end', 'text', 'cntext', 'path']):
            start = tt[i]['start']
            end = tt[i]['end']
            start_ms = convert_time_to_milliseconds(start)
            end_ms = convert_time_to_milliseconds(end)
            if 1000 <= end_ms - start_ms < 15000:
                filtered_tt.append(tt[i])

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


def plot_loudness(file_path, start_time=0, end_time=None):
    """
    绘制音频文件的响度图，并标记左右两侧的最低点

    参数:
    - file_path: 音频文件的路径
    - start_time: 开始时间（秒）
    - end_time: 结束时间（秒），如果为None则到音频末尾
    """
    # 读取音频文件
    y, sr = librosa.load(file_path)

    # 如果end_time为None，则设置为音频文件的总时长
    if end_time is None:
        end_time = len(y) / sr

    # 转换开始和结束时间为样本索引
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)

    # 选择音频的指定部分
    y_segment = y[start_sample:end_sample]

    # 计算短时能量
    frame_length = 2048
    hop_length = 512
    energy = np.array([
        np.sum(np.square(y_segment[i:i + frame_length]))
        for i in range(0, len(y_segment) - frame_length, hop_length)
    ])

    # 计算响度
    loudness = 10 * np.log10(energy + 1e-10)  # 加一个小常数以避免log(0)

    # 创建时间轴
    times = np.arange(len(energy)) * hop_length / sr + start_time

    # 将音频段一分为三分之一
    total_length = len(times)
    left_length = total_length // 3  # 左侧的三分之一
    right_length = total_length // 3  # 右侧的三分之一

    left_loudness = loudness[:left_length]
    right_loudness = loudness[-right_length:]

    # 找到左侧最低点（从start开始遍历）
    left_min_index = np.argmin(left_loudness)
    left_min_time = times[left_min_index]
    left_min_loudness = left_loudness[left_min_index]

    # 找到右侧最低点（从end开始遍历）
    right_min_index = np.argmin(right_loudness)
    right_min_time = times[-right_length + right_min_index]
    right_min_loudness = right_loudness[right_min_index]

    # # 绘制响度图
    # plt.figure(figsize=(12, 6))
    # plt.plot(times, loudness, label='Loudness (dB)')
    # plt.scatter(left_min_time, left_min_loudness, color='red', zorder=5, label='Left Minimum Point')
    # plt.scatter(right_min_time, right_min_loudness, color='blue', zorder=5, label='Right Minimum Point')
    # plt.title('Loudness over Time')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Loudness (dB)')
    # plt.xlim(start_time, end_time)
    # plt.grid()
    # plt.legend()
    #
    # # 标注左侧最低点的值
    # plt.annotate(f'Left Min: {left_min_loudness:.2f} dB',
    #              xy=(left_min_time, left_min_loudness),
    #              xytext=(left_min_time + 0.5, left_min_loudness + 2),
    #              arrowprops=dict(arrowstyle='->', color='red'),
    #              fontsize=10)
    #
    # # 标注右侧最低点的值
    # plt.annotate(f'Right Min: {right_min_loudness:.2f} dB',
    #              xy=(right_min_time, right_min_loudness),
    #              xytext=(right_min_time - 1.5, right_min_loudness + 2),
    #              arrowprops=dict(arrowstyle='->', color='blue'),
    #              fontsize=10)
    #
    # plt.show()

    return left_min_time, right_min_time  # 返回左右两侧最低点的时间


def main_main(url, file):
    # url='https://music.163.com/song?id=1878812258&userid=129707286'
    eng, cn = Toolbox.download_lyr(Toolbox.get_id(url))
    tt = Current_lry.LRY().lry(eng, cn)
    tt = main(tt, file)
    print('分割之后', tt)
    return tt
def convert_milliseconds_to_time(ms):
    """将毫秒转换为时间字符串"""
    milliseconds = ms % 1000
    total_seconds = ms // 1000
    seconds = total_seconds % 60
    minutes = total_seconds // 60

    return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

def convert_time_to_milliseconds(time_str):
    """将时间字符串转换为毫秒"""
    minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split('.')
    return int(minutes) * 60 * 1000 + int(seconds) * 1000 + int(milliseconds)

def main(tt, file):
    # audio = AudioSegment.from_file(file)
    audio = AudioSegment.from_file(file)
    file = file.split('_')[0] + '.mp3'
    audio_with_sound = AudioSegment.from_file(file)
    newt=[]
    for index in range(len(tt)):
        if (all(key in tt[index] for key in ['start', 'end', 'text', 'cntext'])
                and all(tt[index][key] is not None for key in ['start', 'end', 'text', 'cntext'])
                and len(tt[index]['text'].split()) > 3):
            start = convert_time_to_milliseconds(tt[index]['start'])/1000
            end = convert_time_to_milliseconds(tt[index]['end'])/1000
            # print('start',start,'end',end,tt[index])
            # print()
            start -= 1
            end += 0.1
            left_min_time, right_min_time = plot_loudness(file, start_time=start, end_time=end)
            # print(left_min_time)
            # print(right_min_time)
            # plot_spectrogram(file, start_time=start, end_time=end,index=index)

            start_ms = left_min_time * 1000
            end_ms = right_min_time * 1000

            output1 = f"temp/OK1_{index}_{time.time()}.wav"
            output2 = f"temp/OK2_{index}_{time.time()}.wav"

            audio_segment = audio[start_ms:end_ms]
            audio_with_sound_se = audio_with_sound[start_ms:end_ms]
            audio_segment.export(output1, format="wav")
            audio_with_sound_se.export(output2, format="wav")
            tt[index]['path'] = output1
            tt[index]['sound_path'] = output2
            tt[index]['start']=convert_milliseconds_to_time(int(start_ms))


            tt[index]['end']=convert_milliseconds_to_time(int(end_ms))
            newt.append(tt[index])
    print('tt',tt)
    tt=newt
    tt = remove_similar(tt)
    tt = [t for t in tt if 'path' in t]
    return tt