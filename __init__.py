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
import Current_lry

import Toolbox

if __name__ == '__main__':

    music_name = 'HOYO-MiX - Da Capo_noreverb' + '.mp3'  # 在当前目录下的mp3
    url = 'https://music.163.com/song?id=2026565329&userid=129707286'
    dur = 600
    part = 0

    # music_name = os.path.join('music', music_name)
    if Toolbox.check_Cmusic_name(url, music_name):
        pic_path = Toolbox.checking_path(url)
        tks = split_audio.cutting_and_finer_cutting(music_name, part)  # 切割音频并获得更细分的片段
        # tks=[{'path': 'temp\\OK_7.wav', 'text': "I don't feel a single thing"}, {'path': 'temp\\OK_8.wav', 'text': 'Have the pills done too much?'}, {'path': 'temp\\OK_9.wav', 'text': "I've been caught up with my friends in weeks And now we're out of touch I've been driving in that lane"}, {'path': 'temp\\OK_10.wav', 'text': 'And the world feels too big.'}, {'path': 'temp\\OK_11.wav', 'text': "Like a floating ball that's bound to break. Snap my psyche like a twig."}, {'path': 'temp\\OK_14.wav', 'text': 'A little bit tired of quick repairs to cope'}, {'path': 'temp\\OK_15.wav', 'text': "A little bit tired of sinking, there's water in my boat I'm barely breathing, tryna stay afloat, so I got these quick"}, {'path': 'temp\\OK_16.wav', 'text': "We pass to cope. Guess I'm just broken and broke."}, {'path': 'temp\\OK_18.wav', 'text': "The prescription's on its way"}, {'path': 'temp\\OK_19.wav', 'text': "With a name I can't pronounce"}, {'path': 'temp\\OK_20.wav', 'text': 'And the dose I gotta take'}, {'path': 'temp\\OK_23.wav', 'text': "A little bit tired of trying to care when I don't"}, {'path': 'temp\\OK_24.wav', 'text': 'A little bit tired of quick'}, {'path': 'temp\\OK_25.wav', 'text': 'Three pairs to cope.'}, {'path': 'temp\\OK_26.wav', 'text': "A little bit tired, it's sinking, there's water in my boat I'm barely breathing, tryna stay up low So I got these quick repairs to cope Do"}, {'path': 'temp\\OK_28.wav', 'text': 'Get a little bit tired of life.'}, {'path': 'temp\\OK_31.wav', 'text': "It's all the time."}, {'path': 'temp\\OK_33.wav', 'text': "Little bug that's gotta survive"}]

        print(tks)
        index = 0
        # while index < len(tks):
        while index < len(tks):
            file_name_without_ext = os.path.splitext(os.path.basename(tks[index]['path']))[0]  # 获取文件名不含扩展名
            tks[index]['text'], tks[index]['CNtext'] = Current_lry.LRYf().lryF(url, tks[index])
            tks[index]['AItextPath'] = ChatTTS.TTSF().text2speakF(tks[index]['CNtext'], file_name_without_ext)
            tks[index]['middlePath'] = new_audio.control_audioF().combined_Mp3(tks[index]['AItextPath'],
                                                                               tks[index]['path'],
                                                                               file_name_without_ext, dur)
            tks[index]['finaMp4'] = new_audio.control_audioF().combined_all_wav2mp4(tks[index], file_name_without_ext,
                                                                                    pic_path, dur)
            index += 1
        # 根据处理后的数据生成视频
        file = new_audio.control_audioF().make_videos(tks)
        new_audio.control_audio().all_temp(tks)
