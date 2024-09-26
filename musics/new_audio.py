# -*- coding: utf-8 -*-
import shlex
import shutil
import subprocess
import time
import ffmpeg
from pydub import AudioSegment
import os
from concurrent.futures import ThreadPoolExecutor
from moviepy.editor import *
import pysrt


class control_audio():

    def combined_mp3(self, audio_info, file_name_without_ext):

        full_path = os.path.join('temp', f'{int(time.time())}_{file_name_without_ext}.wav')

        combined = AudioSegment.empty()  # 创建一个空的音频段

        for audio_file, silence_duration in audio_info:
            audio = AudioSegment.from_file(audio_file)
            combined += audio  # 添加音频
            combined += AudioSegment.silent(duration=silence_duration)  # 添加静音段

        combined.export(full_path, format="wav")  # 导出合成后的音频
        return full_path

    def adjust_audio_volume(self, input_path, volume_change):
        # 加载音频文件
        audio = AudioSegment.from_file(input_path)

        # 增加音量
        audio = audio + volume_change  # 增加音量，比如 20 dB

        # 导出到新文件
        audio.export(input_path, format='wav')

    def get_audio_duration(self, audio_file_path):
        audio = AudioSegment.from_file(audio_file_path)
        duration_ms = len(audio)  # 播放时长（毫秒）
        # duration_sec = duration_ms / 1000.0  # 转换为秒
        return duration_ms

    def get_Tick(self, t):
        minutes, seconds = t.split(':')
        Tick = int(float(int(minutes) * 60 + float(seconds)) * 1000)
        return Tick

    def safe_list(self, video_paths):
        print('video_paths', video_paths)
        with open('video_list.txt', 'w', encoding='utf-8') as f:
            for video in video_paths:
                f.write(f"file '{video}'\n")

        video_list_path = os.path.abspath('video_list.txt')

        return video_list_path

    def create_background(self, total_ms, file_name_without_ext, pic_path):
        file = os.path.abspath(os.path.join('temp', f'N{int(time.time())}_{file_name_without_ext}.mp4'))
        pic_file = os.path.abspath(pic_path)

        command = [
            'ffmpeg',
            '-y',  # 自动覆盖文件
            '-loop', '1',
            '-i', pic_file,
            '-vf', 'scale=1280x720',  # 设置目标分辨率
            '-c:v', 'libx264',
            '-t', '{}'.format(total_ms / 1000),
            '-pix_fmt', 'yuv420p',
            file
        ]
        subprocess.run(command)
        return file

    def create_audio_movie(self, B, M, file_name_without_ext):
        file = os.path.abspath(os.path.join('temp', f'S{int(time.time())}_{file_name_without_ext}.mp4'))
        command = [
            'ffmpeg',
            '-i', B,
            '-i', M,
            '-y',  # 自动覆盖文件
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            file
        ]  # 融合黑屏和音频

        subprocess.run(command)
        current_directory_file = os.path.join(os.getcwd(), f'S{int(time.time())}_{file_name_without_ext}.mp4')
        shutil.move(file, current_directory_file)

        return f'S{int(time.time())}_{file_name_without_ext}.mp4'

    def create_mp4Withsrt(self, V, S):
        subtitle_file = S
        file = os.path.abspath(os.path.join(f'F{int(time.time())}.mp4'))
        ffmpeg.input(V).output(file, vf='subtitles=' + subtitle_file).run()

        return file, V, S

    def create_src(self, tk, dur):
        subs = pysrt.SubRipFile()
        # subtitle_file = os.path.join('srt', f'{int(time.time())}.srt')
        subtitle_file = f'{int(time.time())}.srt'
        index = 1
        c = control_audio()

        if 'AItextPath' in tk:
            duration_en = c.get_audio_duration(tk['path'])

            duration_cn = c.get_audio_duration(tk['AItextPath'])

            eng_begin = duration_en + dur + duration_cn + dur
            cn_begin = duration_en + dur

            # 添加中文字幕
            subs.append(pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=cn_begin / 1000),
                end=pysrt.SubRipTime(seconds=(cn_begin + duration_cn) / 1000),
                text=tk['CNtext']
            ))
            index += 1
            subs.append(pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=cn_begin / 1000),
                end=pysrt.SubRipTime(seconds=(cn_begin + duration_cn) / 1000),
                text=tk['text']
            ))
            index += 1

            subs.append(pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=eng_begin / 1000),
                end=pysrt.SubRipTime(seconds=(eng_begin + duration_en) / 1000),
                text=tk['text']
            ))
            index += 1
            subs.append(pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=eng_begin / 1000),
                end=pysrt.SubRipTime(seconds=(eng_begin + duration_en) / 1000),
                text=tk['CNtext']
            ))

            # 保存到 SRT 文件
        subs.save(subtitle_file, encoding='utf-8')

        return subtitle_file

    def all_temp(self, tks):
        for tk in tks:
            os.remove(tk['path'])
            os.remove(tk['AItextPath'])
            os.remove(tk['middlePath'])
            os.remove(tk['finaMp4'])


class control_audioF():

    def make_videos(self, tks):
        file = os.path.abspath(os.path.join('finsh', f'{int(time.time())}.mp4'))
        c = control_audio()
        te = []
        for i in tks:
            if 'finaMp4' in i:
                # 如果键存在，可以安全地访问它
                te.append(i['finaMp4'])

        video_list_path = c.safe_list(te)
        # print('video_list_path', video_list_path)
        # 使用FFmpeg合成视频
        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', video_list_path,
            '-c:v', 'libx264',  # 使用 H.264 编码
            '-c:a', 'aac',  # 使用 AAC 编码
            '-b:v', '2000k',  # 设置视频比特率
            '-b:a', '192k',  # 设置音频比特率
            '-y',
            file
        ]

        subprocess.run(command, check=True)
        print(tks)
        return file

        # full_path = os.path.join(path, f'{int(time.time())}.wav')

    def combined_Mp3(self, Vpath, Dpath, file_name_without_ext, dur):
        c = control_audio()
        control_audio().adjust_audio_volume(Vpath, 10)

        audio_info = [
            (Dpath, dur),  # 使用减慢速度的音频
            (Vpath, dur),
            (Dpath, dur),
            ("叮.mp3", dur)
        ]
        middle_wav_path = c.combined_mp3(audio_info, file_name_without_ext)
        return os.path.abspath(middle_wav_path)

    def combined_all_wav2mp4(self, tk, file_name_without_ext, pic_path, dur):
        c = control_audio()
        # subtitle_file = c.create_src(tk, dur, file_name_without_ext)
        total_ms = c.get_audio_duration(tk['middlePath'])
        src = c.create_src(tk, dur)
        backgroundOnly = c.create_background(total_ms, file_name_without_ext, pic_path)
        backgroundWithWav = c.create_audio_movie(backgroundOnly, tk['middlePath'], file_name_without_ext)

        final, V, S = c.create_mp4Withsrt(backgroundWithWav, src)
        os.remove(V)
        os.remove(S)
        os.remove(backgroundOnly)
        return final


if __name__ == '__main__':
    c1 = control_audioF()
    c2 = control_audio()
    tks = [{'path': 'temp\\OK_0.wav',
            'text': "I threw a wish in the well, don't ask me I'll never tell, I looked at you as it fell"},
           {'path': 'temp\\OK_1.wav', 'text': "And now you're in my way"},
           {'path': 'temp\\OK_2.wav', 'text': 'I trade my soul for a wish'}]
    # for tk in tks:
    tk = tks[0]
    tk['AItextPath'] = 'temp\\V1727326293_OK_0.wav'
    src = c2.create_src(tk, 600)
    print('src', src)
    end = c2.create_mp4Withsrt('S1727326296_OK_0.mp4', src)
    # print('end', end)
