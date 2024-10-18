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
from PIL import Image
import pic_making
import cover_making
import add_content


class control_audio():

    def combined_mp3(self, audio_info, file_name_without_ext):

        full_path = os.path.join('temp', f'{time.time()}_{file_name_without_ext}.wav')

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
        # print('video_paths', video_paths)
        with open('video_list.txt', 'w', encoding='utf-8') as f:
            for video in video_paths:
                f.write(f"file '{video}'\n")

        video_list_path = os.path.abspath('video_list.txt')

        return video_list_path

    def get_image_resolution(self, pic_file):
        with Image.open(pic_file) as img:
            return img.size  # 返回 (宽度, 高度)

    def create_background(self, total_ms, file_name_without_ext, pic_path):

        file = os.path.abspath(os.path.join('temp', f'N{int(time.time())}_{file_name_without_ext}.mp4'))
        pic_file = os.path.abspath(pic_path)

        resolution = cover_making.get_image_resolution(pic_file)
        clip = ImageClip(pic_file).set_duration(total_ms / 1000)
        clip = clip.resize(newsize=resolution)
        clip.write_videofile(file, fps=6)

        return file

    def create_audio_movie(self, B, M):
        t = int(time.time())
        file = os.path.abspath(os.path.join('temp', f'S{t}.mp4'))
        # file = os.path.abspath(os.path.join('temp', f'S{int(time.time())}_{file_name_without_ext}.mp4'))
        command = [
            'ffmpeg',
            '-i', B,
            '-i', M,
            '-y',  # 自动覆盖文件
            # '-c:v', 'copy',
            # '-c:a', 'aac',
            # '-strict', 'experimental',
            file
        ]  # 融合黑屏和音频

        subprocess.run(command)
        current_directory_file = os.path.join(os.getcwd(), f'S{t}.mp4')
        shutil.move(file, current_directory_file)

        return f'S{t}.mp4'

    def create_mp4Withsrt(self, V, S):
        subtitle_file = S
        file = os.path.abspath(os.path.join(f'F{int(time.time())}.mp4'))
        print('file', file, 'subtitle_file', subtitle_file, 'V', V)
        ffmpeg.input(V).output(file, vf='subtitles=' + subtitle_file).run()

        return file, V, S

    def create_src(self, tk, dur):
        subs = pysrt.SubRipFile()
        # subtitle_file = os.path.join('srt', f'{int(time.time())}.srt')
        subtitle_file = f'{int((time.time()))}.srt'
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
                text=tk['text']
            ))
            index += 1
            subs.append(pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=cn_begin / 1000),
                end=pysrt.SubRipTime(seconds=(cn_begin + duration_cn) / 1000),
                text=tk['CNtext']
            ))
            index += 1
            subs.append(pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=eng_begin / 1000),
                end=pysrt.SubRipTime(seconds=(eng_begin + duration_en) / 1000),
                text=tk['CNtext']
            ))
            index += 1
            subs.append(pysrt.SubRipItem(
                index=index,
                start=pysrt.SubRipTime(seconds=eng_begin / 1000),
                end=pysrt.SubRipTime(seconds=(eng_begin + duration_en) / 1000),
                text=tk['text']
            ))

            # 保存到 SRT 文件
        subs.save(subtitle_file, encoding='utf-8')

        return subtitle_file

    def delete_all_files_in_cover_output(self, cover_output_path):
        for filename in os.listdir(cover_output_path):
            file_path = os.path.join(cover_output_path, filename)
            if os.path.isfile(file_path):  # 确保是文件
                os.remove(file_path)

    def all_temp(self, tks):
        for tk in tks:
            # 检查并删除 tiktokMp4 文件
            tiktok_file = tk['tiktokMp4']
            if os.path.exists(tiktok_file):
                os.remove(tiktok_file)

            # 检查并删除 biliMp4 文件
            bili_file = tk['biliMp4']
            if os.path.exists(bili_file):
                os.remove(bili_file)
        self.delete_all_files_in_cover_output('temp')
        self.delete_all_files_in_cover_output('cover_output')

    def HC(self, video_list_path, bili):
        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', video_list_path,
            '-y',  # 始终覆盖输出文件
            f"{bili.split('.')[0]}_F.mp4"
        ]
        subprocess.run(command, check=True)

        return f"{bili.split('.')[0]}_F.mp4"

    def move2last(self, combined_video):
        file_name = os.path.basename(combined_video)
        destination = os.path.join(os.getcwd(), file_name)
        shutil.move(combined_video, destination)
        return destination

    def change_speed(self, file):
        original_audio = AudioSegment.from_file(file)
        speed_changed_audio = original_audio.speedup(playback_speed=1.2)

        basename = os.path.basename(file)  # 获取文件名部分

        result=os.path.join('temp',basename[:-4] +'Speed'+'.wav')
        # 导出处理后的音频为临时文件

        speed_changed_audio.export(result, format="wav")
        print('result',result)
        return result
        # 更新 audio_info 使用处理后的音频


class control_audioF():

    def make_videos(self, tks, music_name, pic_path_tiktok_, pic_path_bili_):
        def process_video(platform, pic_path, video_key, output_folder):
            # 创建视频
            pic_path = cover_making.create_background(cover_making.main(platform, pic_path))

            # 获取视频路径
            video_paths = [i[video_key] for i in tks]  # 使用列表推导式获取视频路径
            video_list_path = control_audio().safe_list(video_paths)

            # 生成视频文件的完整路径
            output_path = os.path.abspath(os.path.join(output_folder, f'{music_name}_{platform}.mp4'))

            # 合成音频和视频
            combined_video_before = control_audio().HC(video_list_path, output_path)

            combined_video_before = control_audio().move2last(combined_video_before)

            # combined_video_before = add_content.add_text2video(combined_video_before)

            pic_path = control_audio().move2last(pic_path)

            final_video_list = [pic_path, combined_video_before]

            video_list_path = control_audio().safe_list(final_video_list)
            # print('video_list_path', video_list_path)
            combined_video = control_audio().HC(video_list_path, combined_video_before)

            new_location = os.path.join(os.getcwd(), output_folder, os.path.basename(combined_video))
            shutil.move(combined_video, new_location)

            os.remove(combined_video_before)
            os.remove(pic_path)

            combined_video = add_content.add_text2video(new_location, music_name)
            os.remove(new_location)
            return combined_video

        # 处理 Bilibili 视频
        bili_video = process_video('b', pic_path_bili_, 'biliMp4', 'finish_bili')

        # 处理 TikTok 视频
        tik_video = process_video('dy', pic_path_tiktok_, 'tiktokMp4', 'finish_dy')
        # bili_video
        # tik_video
        # return bili_video, tik_video
        return bili_video, tik_video

        # full_path = os.path.join(path, f'{int(time.time())}.wav')

    def combined_Mp3(self, Vpath, Dpath, file_name_without_ext, dur,Sound):
        # Vpath = control_audio().change_speed(Vpath)
        # Dpath2=control_audio().change_speed(Dpath)
        # Dpath1 = control_audio().change_speed(Dpath, 1.4)
        control_audio().adjust_audio_volume(Vpath, 7)
        audio_info = [
            (Dpath, dur),
            (Vpath, dur),
            (Dpath, dur+dur),
            (Sound, dur),
            ("resource/叮.mp3", dur),
        ]
        middle_wav_path = control_audio().combined_mp3(audio_info, file_name_without_ext)
        return os.path.abspath(middle_wav_path)

    def combined_all_wav2mp4(self, tk, file_name_without_ext, dur, pic_path_tiktok, pic_path_bili):
        total_ms = control_audio().get_audio_duration(tk['middlePath'])
        src = control_audio().create_src(tk, dur)

        backgroundOnly_tik = control_audio().create_background(total_ms, file_name_without_ext, pic_path_tiktok)
        backgroundWithWav_tik = control_audio().create_audio_movie(backgroundOnly_tik, tk['middlePath'])

        final1, V1, S1 = control_audio().create_mp4Withsrt(backgroundWithWav_tik, src)

        backgroundOnly_bili = control_audio().create_background(total_ms, file_name_without_ext, pic_path_bili)
        backgroundWithWav_bili = control_audio().create_audio_movie(backgroundOnly_bili, tk['middlePath'])
        final2, V2, S2 = control_audio().create_mp4Withsrt(backgroundWithWav_bili, src)
        # os.remove(S1)
        #
        # os.remove(V1)
        # os.remove(V2)
        return final1, final2

    def make_longer_videos(self, music_name):
        # 获取 finsh 文件夹的绝对路径
        finsh_dir = os.path.abspath('finsh')

        # 读取 finsh 文件夹下的所有文件

        # 如果需要过滤特定类型的文件，可以使用以下方式
        mp4_files = [
            os.path.join(finsh_dir, file)
            for file in os.listdir(finsh_dir)
            if file.endswith('.mp4')
        ]

        file = os.path.abspath(os.path.join(finsh_dir, f'{music_name}.mp4'))
        c = control_audio()

        video_list_path = c.safe_list(mp4_files)

        # 使用 FFmpeg 合成视频
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
        return file


if __name__ == '__main__':
    import Toolbox

    url = 'https://music.163.com/song?id=1810305356'
    mode = 'dy'
    pic_path = Toolbox.checking_path(url, mode)
    print('pic_path', pic_path)
    resolution = control_audio().get_image_resolution(pic_path)
    print(resolution)
    print(control_audio().create_background(5, '123', pic_path))
#     c1 = control_audioF()
#     c2 = control_audio()
#     tks = [{'path': 'temp\\OK_0.wav',
#             'text': "I threw a wish in the well, don't ask me I'll never tell, I looked at you as it fell"},
#            {'path': 'temp\\OK_1.wav', 'text': "And now you're in my way"},
#            {'path': 'temp\\OK_2.wav', 'text': 'I trade my soul for a wish'}]
#     # for tk in tks:
#     tk = tks[0]
#     tk['AItextPath'] = 'temp\\V1727326293_OK_0.wav'
#     src = c2.create_src(tk, 600)
#     print('src', src)
#     end = c2.create_mp4Withsrt('S1727326296_OK_0.mp4', src)
#     # print('end', end)
