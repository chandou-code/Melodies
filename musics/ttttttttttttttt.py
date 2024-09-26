# -*- coding: utf-8 -*-
import shlex
import subprocess
import time

import whisperwhisper
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os


def list_temp_files():
    temp_dir = 'temp'  # 当前目录下的 temp 文件夹
    try:
        # 获取 temp 目录下的所有文件和文件夹
        files = os.listdir(temp_dir)
        # 过滤出文件
        files = [f for f in files if os.path.isfile(os.path.join(temp_dir, f))]

        print("temp 目录下的文件:")
        for file in files:
            os.remove(os.path.join(temp_dir, file))
    except Exception as e:
        print(f"发生错误: {e}")


def cutting_and_finer_cutting(input_file):
    path = f'temp'

    sound = AudioSegment.from_mp3(input_file)
    loudness = sound.dBFS
    duration_ms = len(sound)
    silence_thresh = loudness - 10

    if duration_ms > 60000:
        min_silence_len = 700
        keep_silence = 400
    else:
        min_silence_len = 500
        keep_silence = 300

    chunks = split_on_silence(sound,
                              min_silence_len=min_silence_len,
                              silence_thresh=silence_thresh,
                              keep_silence=keep_silence)

    start_time = 0
    tks = []
    for i, chunk in enumerate(chunks):
        audio_info = {}
        end_time = start_time + len(chunk)
        file_name = os.path.join(path, f"cutwav_{i}.wav")

        if len(chunk) <= 20000:
            chunk.export(file_name, format="wav")
            audio_info['dur'] = (start_time, end_time)
            audio_info['path'] = file_name
            print('len(chunk) <= 20000', file_name)
            # audio_info['text'] = ''
            tks.append(audio_info)
            start_time = end_time

        if len(chunk) > 20000:
            finer_chunks = split_on_silence(chunk,
                                            min_silence_len=300,
                                            silence_thresh=silence_thresh,
                                            keep_silence=200)
            print('finer_chunks', finer_chunks)
            finer_start_time = start_time - len(chunk)
            # os.remove(file_name)  # 删除父文件
            # os.remove(audio_info['path'])  # 删除父文件
            # tks.pop()

            for j, finer_chunk in enumerate(finer_chunks):
                finer_file_name = os.path.join(path, f"cutwav_{i}_finer_{j}.wav")

                finer_chunk.export(finer_file_name, format="wav")
                finer_end_time = finer_start_time + len(finer_chunk)
                audio_info['dur'] = (finer_start_time, finer_end_time)
                audio_info['path'] = finer_file_name
                # audio_info['text'] = ''
                tks.append(audio_info)
                finer_start_time = finer_end_time

    return tks

def create_mp4Withsrt():
    # print(V)
    # print(os.path.abspath(S))

    file = os.path.abspath(os.path.join('temp', f'F{int(time.time())}.mp4'))
    # 已知的 srt 文件路径
    srt_file_path = r'myproject\musics\srt\1727312055.srt'

    # 构造 FFmpeg 字符串
    ffmpeg_subtitle_string = "'{}'".format(srt_file_path.replace('\\', '\\\\'))
    ttt='"'+'subtitles='+ffmpeg_subtitle_string+'"'
    print()
    # 输出结果
    # print(ffmpeg_subtitle_string)

    command = [
        'ffmpeg',
        '-i', r'C:\Users\10717\PycharmProjects\pythonProject3\myproject\musics\temp\123.mp4',
        '-vf',
        # f'subtitles={escaped_SPATH}:force_style=\'Alignment=2,OutlineColour=&H100000000,BorderStyle=1,Outline=1,Shadow=0,Fontsize=8,MarginL=10,MarginV=15\'',
        ttt,
        file
    ]

    # print(command)  # 调试输出命令
    subprocess.run(command)
    # os.remove(V)
    return file
def pf():
    import ffmpeg

    # 输入视频文件路径
    input_video = r'C:\Users\10717\PycharmProjects\pythonProject3\myproject\musics/123.mp4'
    # 字幕文件路径 (如 .srt 或 .ass)
    # subtitle_file = r'\srt\1727326582.srt'
    subtitle_file = r'\1727326295.srt'
    # 输出视频文件路径
    output_video = 'output_video.mp4'

    # 使用 ffmpeg 添加硬字幕
    ffmpeg.input(input_video).output(output_video, vf='subtitles=' + subtitle_file).run()
# 示例调用`
if __name__ == '__main__':
    # info = cutting_and_finer_cutting("OneRepublic - Counting Stars_noreverb.mp3")
    # # index = 0
    # # while index < len(info):
    # #     info[0]['text'] = whisperwhisper.WF().translationF(info[0]['path'])
    # #     index += 1
    # print(info)
    # create_mp4Withsrt()
    pf()