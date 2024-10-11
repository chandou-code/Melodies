# -*- coding: utf-8 -*-
import os
import glob
def clearing():
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 删除所有.srt文件
    srt_files = glob.glob(os.path.join(current_directory, '*.srt'))
    for srt_file in srt_files:
        os.remove(srt_file)
        print(f"Deleted: {srt_file}")

    # 指定不想删除的mp4文件名（不包括扩展名）
    files_to_exclude = ['file1', 'file2']  # 替换为需要排除的文件名

    # 删除筛选后的所有.mp4文件
    mp4_files = glob.glob(os.path.join(current_directory, '*.mp4'))
    for mp4_file in mp4_files:
        file_name_without_ext = os.path.splitext(os.path.basename(mp4_file))[0]
        if file_name_without_ext not in files_to_exclude:
            os.remove(mp4_file)
            print(f"Deleted: {mp4_file}")