# -*- coding: utf-8 -*-
import shutil
from collections import Counter
import whisperwhisper
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import whisperwhisper
import search


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


def cutting_and_finer_cutting(input_file, part):
    path = f'temp'

    sound = AudioSegment.from_mp3(input_file)
    loudness = sound.dBFS
    duration_ms = len(sound)
    silence_thresh = loudness - 10

    # chunks = split_on_silence(sound,
    #                           min_silence_len=340,
    #                           silence_thresh=silence_thresh,
    #                           keep_silence=240)
    chunks = split_on_silence(sound,
                              min_silence_len=320,
                              silence_thresh=silence_thresh,
                              keep_silence=220)

    tks = []
    index = 0
    remove_tks = []
    # while index < len(chunks):
    # while index < len(chunks):
    if part == 0:
        part = len(chunks)
    print(f'切割个数:{len(chunks)}')
    while index < part:
        chunk = chunks[index]
        # 过滤掉长度小于1秒的片段
        if len(chunk) < 800:  # 小于1000毫秒，即1秒
            # print(f'忽略小于1秒的片段: {len(chunk) / 1000}秒')
            index += 1
            continue

        audio_info = {}
        file = os.path.join(path, f"TEMP_{index}.wav")
        chunk.export(file, format="wav")

        try:
            text = whisperwhisper.WF().translationF(file)
        except UnicodeEncodeError as e:
            print(f"忽略错误: {e}")
            index += 1
            continue
        except Exception as e:
            print(f"其他错误: {e}, 跳过文件: {file}")
            index += 1
            continue
        if text == '' or text is None:
            index += 1
            continue
        word_count_c = len(text.split())
        word_count = Counter(text.split())

        # 计算重复单词的个数
        repeated_count = sum(1 for count in word_count.values() if count > 1)

        # print('before', text, word_count)
        if word_count_c < 4 or repeated_count > 3:
            print('noway', text, word_count)
            index += 1

            remove_tks.append(file)
            continue
        if any(word in text for word in ['Yeah', 'haha', 'yeah', 'oh', 'OH', 'Oh']):
            print('noway', text, word_count)
            index += 1

            remove_tks.append(file)
            continue

        file_name = os.path.join(path, f'OK_{index}.wav')
        shutil.move(file, file_name)

        chunk.export(file_name, format="wav")
        print('ok', text, word_count)
        audio_info['path'] = file_name
        audio_info['text'] = text
        tks.append(audio_info)
        index += 1
    del_file(remove_tks)
    tks = search.remove_if_similar(tks)
    return tks


def del_file(remove_tks):
    for file_path in remove_tks:
        try:

            if os.path.isfile(file_path['path']):  # 检查文件是否存在
                os.remove(file_path['path'])  # 删除文件
                print(f"已删除: {file_path}")
            else:
                print(f"文件不存在: {file_path}")
        except Exception as e:
            print(f"删除文件时出错: {file_path}, 错误信息: {e}")





# 示例调用`
if __name__ == '__main__':
    info, remove_tks = cutting_and_finer_cutting("music/Carly Rae Jepsen - Call Me Maybe_noreverb.mp3")
    # index = 0
    # while index < len(info):
    #     info[0]['text'] = whisperwhisper.WF().translationF(info[0]['path'])
    #     index += 1

    print(info)
