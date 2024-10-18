# -*- coding: utf-8 -*-
import os
import subprocess
# import os
import ffmpeg

# 示例用法
# plot_spectrogram('your_audio_file.wav', start_time=1, end_time=2)
import shlex
import shutil
import subprocess
import time
import ffmpeg
from pydub import AudioSegment

import librosa.display

from scipy.signal import butter, filtfilt
from scipy.ndimage import gaussian_filter

import librosa
import librosa.display


import numpy as np
import librosa
import matplotlib.pyplot as plt

def get_info(tk):
    # 获取视频的详细信息
    try:
        probe = ffmpeg.probe(tk)

        # 打印基本信息
        print("视频基本信息:")
        print(f"文件名: {probe['format']['filename']}")
        print(f"文件大小: {int(probe['format']['size']) / (1024 * 1024):.2f} MB")
        print(f"时长: {float(probe['format']['duration']):.2f} 秒")
        print(f"比特率: {int(probe['format']['bit_rate']) / 1000:.2f} kbps")

        # 打印视频流信息
        for stream in probe['streams']:
            if stream['codec_type'] == 'video':
                print("\n视频流信息:")
                print(f"编码格式: {stream['codec_name']}")
                print(f"分辨率: {stream['width']}x{stream['height']}")
                print(f"帧率: {stream['r_frame_rate']}")
                print(f"像素格式: {stream['pix_fmt']}")
                print(f"时长: {float(stream['duration']):.2f} 秒")
                print(f"比特率: {stream['bit_rate']} bps")

            elif stream['codec_type'] == 'audio':
                print("\n音频流信息:")
                print(f"编码格式: {stream['codec_name']}")
                print(f"声道数: {stream['channels']}")
                print(f"采样率: {stream['sample_rate']} Hz")
                print(f"比特率: {stream['bit_rate']} bps")

    except ffmpeg.Error as e:
        print("获取视频信息时出错:", e)






def plot_spectrogram(audio_file, start_time, end_time, index, sr=None):
    y, sr = librosa.load(audio_file, sr=sr)
    duration = librosa.get_duration(y=y, sr=sr)
    if start_time < 0 or end_time > duration or start_time >= end_time:
        raise ValueError(f"时间范围无效：音频长度为 {duration:.2f} 秒，输入的范围为 [{start_time}, {end_time}] 秒。")

    y_segment = y[int(start_time * sr):int(end_time * sr)]
    # print(y_segment)
    # 低通滤波
    b, a = butter(16, 0.5, btype='low', analog=False)
    y_filtered = filtfilt(b, a, y_segment)

    # 计算STFT，增加n_fft和减少hop_length
    D = librosa.stft(y_filtered, n_fft=2048, hop_length=512)
    DB = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    # 平滑声谱图
    DB_smooth = gaussian_filter(DB, sigma=12)

    # 绘制声谱图
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(DB_smooth, sr=sr, x_axis='time', y_axis='log',
                             hop_length=512, x_coords=np.linspace(start_time, end_time, DB_smooth.shape[1]))
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Spectrogram from {start_time}s to {end_time}s')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.ylim(20, 20000)
    plt.grid()
    # 保存到本地
    plt.savefig(f'temp/{index}.png', bbox_inches='tight', dpi=300)  # 指定文件名和分辨率
    plt.show()




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

    # 绘制响度图
    plt.figure(figsize=(12, 6))
    plt.plot(times, loudness, label='Loudness (dB)')
    plt.scatter(left_min_time, left_min_loudness, color='red', zorder=5, label='Left Minimum Point')
    plt.scatter(right_min_time, right_min_loudness, color='blue', zorder=5, label='Right Minimum Point')
    plt.title('Loudness over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Loudness (dB)')
    plt.xlim(start_time, end_time)
    plt.grid()
    plt.legend()

    # 标注左侧最低点的值
    plt.annotate(f'Left Min: {left_min_loudness:.2f} dB',
                 xy=(left_min_time, left_min_loudness),
                 xytext=(left_min_time + 0.5, left_min_loudness + 2),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=10)

    # 标注右侧最低点的值
    plt.annotate(f'Right Min: {right_min_loudness:.2f} dB',
                 xy=(right_min_time, right_min_loudness),
                 xytext=(right_min_time - 1.5, right_min_loudness + 2),
                 arrowprops=dict(arrowstyle='->', color='blue'),
                 fontsize=10)

    plt.show()

    return left_min_time, right_min_time  # 返回左右两侧最低点的时间

def plot_loudness_and_derivatives(file_path, start_time=0, end_time=None):
    """
    绘制音频文件的响度图，并标记响度的一阶和二阶导数

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

    # 计算响度的一阶和二阶导数
    first_derivative = np.gradient(loudness, times)
    second_derivative = np.gradient(first_derivative, times)

    # 绘制响度和导数
    plt.figure(figsize=(12, 8))

    # 绘制响度
    plt.subplot(3, 1, 1)
    plt.plot(times, loudness, label='Loudness (dB)', color='black')
    plt.title('Loudness over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Loudness (dB)')
    plt.grid()
    plt.legend()

    # 绘制一阶导数
    plt.subplot(3, 1, 2)
    plt.plot(times, first_derivative, label='First Derivative (dB/s)', color='orange')
    plt.title('First Derivative of Loudness')
    plt.xlabel('Time (s)')
    plt.ylabel('First Derivative (dB/s)')
    plt.grid()
    plt.legend()

    # 绘制二阶导数
    plt.subplot(3, 1, 3)
    plt.plot(times, second_derivative, label='Second Derivative (dB/s^2)', color='red')
    plt.title('Second Derivative of Loudness')
    plt.xlabel('Time (s)')
    plt.ylabel('Second Derivative (dB/s^2)')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()
# def main():
#     start = float(tks[index]['start'].split(':')[-1].lstrip("0"))  # 先转换为浮点数
#     end = float(tks[index]['end'].split(':')[-1].lstrip("0"))
#
#     print(start)
#     print(end)
#     start -= 1
#     end += 0.1
#     file = 'music/Kelly Clarkson - Stronger_noreverb.mp3'
#     audio = AudioSegment.from_file(file)
#     left_min_time, right_min_time = plot_loudness(file, start_time=start, end_time=end)
#     print(left_min_time)
#     print(right_min_time)
#     # plot_spectrogram(file, start_time=start, end_time=end,index=index)
#     start_ms = left_min_time * 1000
#     end_ms = right_min_time * 1000
#
#     audio_segment = audio[start_ms:end_ms]
#     audio_segment.export('temp/t1.wav', format="wav")



