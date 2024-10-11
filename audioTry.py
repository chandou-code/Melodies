# -*- coding: utf-8 -*-
import os
import subprocess
# import os
import ffmpeg
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


def HC(video_list_path, bili):
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', video_list_path,
        '-y',  # 始终覆盖输出文件
        bili
    ]
    subprocess.run(command, check=True)
    print('video_list_path', video_list_path)
    return bili
import new_audio

if __name__ == '__main__':
    def count_lines_of_code(directory):
        total_lines = 0

        # 遍历目录中的所有文件
        for filename in os.listdir(directory):
            if filename.endswith('.py'):  # 只处理 .py 文件
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    total_lines += len(lines)  # 统计行数

        return total_lines


    # 获取当前目录
    current_directory = os.getcwd()
    lines_count = count_lines_of_code(current_directory)

    print(f"当前目录下所有 .py 文件的代码行数总和: {lines_count}")