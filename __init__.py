# -*- coding: utf-8 -*-
import os
import json  # 导入JSON模块
import translation  # 导入翻译模块
import lyric_handle  # 导入歌词处理模块
import MSST  # 导入MSST模块（具体功能不明）
import ChatTTS  # 导入文本转语音模块
import split_audio  # 导入音频切割模块
import whisperwhisper  # 导入语音识别模块
import new_audio  # 导入新音频处理模块

if __name__ == '__main__':
    music_name = 'music/Carly Rae Jepsen - Call Me Maybe_noreverb.mp3'  # 定义音乐文件名
    pic_path = 'pic/28575553.jpg'
    dur = 600
    part = 0
    tks, remove_tks = split_audio.cutting_and_finer_cutting(music_name, part)  # 切割音频并获得更细分的片段
    split_audio.del_file(remove_tks)
    print(tks)
    index = 0
    # while index < len(tks):
    while index < len(tks):
        file_name_without_ext = os.path.splitext(os.path.basename(tks[index]['path']))[0]  # 获取文件名不含扩展名

        # # 识别音频片段中的文本
        # tks[index]['text'] = whisperwhisper.WF().translationF(tks[index]['path'])

        # 将识别出的文本翻译成中文
        tks[index]['CNtext'] = translation.baiduTranslate_F().baiduTranslate(tks[index]['text'])

        # 将翻译后的中文文本转成语音
        tks[index]['AItextPath'] = ChatTTS.TTSF().text2speakF(tks[index]['CNtext'], file_name_without_ext)

        # 合并生成的语音与原音频
        tks[index]['middlePath'] = new_audio.control_audioF().combined_Mp3(tks[index]['AItextPath'],
                                                                           tks[index]['path'],
                                                                           file_name_without_ext, dur)
        # 将合并的音频转换成的MP4格式
        tks[index]['finaMp4'] = new_audio.control_audioF().combined_all_wav2mp4(tks[index], file_name_without_ext,
                                                                                pic_path, dur)
        index += 1

    print(tks)

    # 根据处理后的数据生成视频
    file = new_audio.control_audioF().make_videos(tks)
    new_audio.control_audio().all_temp(tks)
