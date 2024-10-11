# -*- coding: utf-8 -*-
import re

from PIL import Image
import shutil
from ncmdump import NeteaseCloudMusicFile
import requests
import urllib.parse
import glob
from gradio_client import Client, handle_file
import os
import json

from pydub import AudioSegment

import Current_lry
import pic_making


def pict(image_path):
    # 打开图片

    image = Image.open(image_path)

    # 获取图片尺寸
    width, height = image.size

    # 计算裁剪区域的坐标
    left = (width - 1280) // 2
    upper = (height - 720) // 2
    right = left + 1280
    lower = upper + 720
    crop_box = (left, upper, right, lower)

    # 裁剪图片
    cropped_image = image.crop(crop_box)

    # 保存裁剪后的图片
    cropped_image.save(image_path)

    # 显示裁剪后的图片（可选）
    # cropped_image.show()


def convert_flac_to_mp3(flac_file_path, mp3_file_path):
    # 读取 FLAC 文件
    audio = AudioSegment.from_file(flac_file_path, format='flac')

    # 导出为 MP3 文件
    audio.export(mp3_file_path, format='mp3')


def is_flac_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'fLaC'
    except Exception as e:
        print(f"无法检查文件: {e}")
        return False


def turning(name):
    file_path = os.path.join('music', f"{name}.ncm")
    FLAC = os.path.join('music', f"{name}.flac")
    endname = os.path.join('music', f"{name}.mp3")
    print('FLAC1', FLAC)
    # print(file_path)
    if os.path.exists(FLAC):
        convert_flac_to_mp3(FLAC, endname)
    if os.path.exists(file_path):

        ncmfile = NeteaseCloudMusicFile(os.path.join('music', f"{name}.ncm"))
        ncmfile.decrypt()
        print(ncmfile.music_metadata)

        names = ncmfile.dump_music(endname)
        if is_flac_file(names):

            convert_flac_to_mp3(FLAC, endname)


    return name


def transform_string(input_str):
    # 移除逗号和空格
    return input_str.replace(',', '').replace('$', '').replace(r"'", '').replace('(', '').replace(')', '')


class MSST():
    def depart(self, name):

        fine_name = transform_string(f'{name}_noreverb.mp3')
        nn = os.path.join('music', f'{name}.mp3')

        music_path = os.path.join(os.getcwd(), 'music', fine_name)
        if not os.path.exists(music_path):
            client = Client("http://localhost:7860/")
            result = client.predict(
                selected_model='dereverb_mel_band_roformer_less_aggressive_anvuew_sdr_18.8050.ckpt',
                input_audio=[handle_file(nn)],
                store_dir="results/",
                extract_instrumental=False,
                gpu_id="0",
                output_format="mp3",
                force_cpu=False,
                use_tta=False,
                api_name="/run_inference_single"
            )
            # path = rf'E:\MSST WebUI\results\{fine_name}'
            results_directory = r'E:\MSST WebUI\results\*'  # 添加 * 来匹配所有文件

            # 获取所有文件
            file = glob.glob(results_directory)[0]

            shutil.move(file, music_path)
            return music_path
        else:
            return music_path


class MSSTF():
    def departF(self, name):
        name = turning(name)  # ncm2mp3
        return MSST().depart(name)
        # return name


def get_data(ids):
    # 定义文件名
    path = 'data'
    filename = f'{ids}.json'
    file_name = os.path.join(path, filename)

    # 检查文件是否存在
    if os.path.exists(file_name):
        print(f'文件 {file_name} 已存在，正在读取...')
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data

    # 如果文件不存在，则进行请求
    url = f'https://music.163.com/api/song/detail?ids=[{ids}]'
    r = requests.get(url)

    # 检测请求是否成功
    if r.status_code == 200:
        data = r.json()

        # 将响应数据存储到 JSON 文件中
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data
    else:
        print("请求失败，状态码:", r.status_code)
        return None


def get_pic(data):
    return data["songs"][0]["album"]["blurPicUrl"]


def download_pic(name, url):
    # 设定存放图片的目录
    directory = "pic"

    # 确保目录存在
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 本地保存的文件名
    file_name = os.path.join(directory, f"{name}.jpg")

    # 检查文件是否存在
    if os.path.exists(file_name):
        return file_name

    # 发送请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 保存图片到本地
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return file_name
    else:
        print("下载图片失败")


def download_lyr(ids):
    # 创建目录/lry，如果不存在
    directory = './lry'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 定义文件路径
    file_path = os.path.join(directory, f'{ids}.json')

    # 检查文件是否存在
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            eng = data['eng']
            cn = data['cn']
            # print(f'使用缓存的文件: {file_path}')
            # print(eng, cn)
            return eng, cn
    else:
        # 文件不存在，进行网络请求
        url1 = f'https://music.163.com/api/song/media?id={ids}'
        url2 = f'https://music.163.com/api/song/lyric?os=pc&id={ids}&lv=-1&tv=-1'

        # print(url2)
        # print(url1)
        # 请求英文歌词
        r1 = requests.get(url1)
        eng = r1.json().get('lyric', '')

        # 请求中文歌词
        r2 = requests.get(url2)
        cn = r2.json().get('tlyric', {}).get('lyric', '')

        # 保存到JSON文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({'eng': eng, 'cn': cn}, file, ensure_ascii=False, indent=4)

        print(f'已下载并保存歌词到: {file_path}')
        return eng, cn


def get_id(url):
    # url = 'https://music.163.com/song?id=25706368&userid=129707286'

    # 解析 URL
    parsed_url = urllib.parse.urlparse(url)

    # 提取查询参数
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # 获取 id 的值
    song_id = query_params.get('id', [None])[0]

    return song_id


def checking_path(url, mode):
    path = download_pic(get_id(url), get_pic(get_data(get_id(url))))
    path = pic_making.image_main(path, mode)
    return path


import Current_lry


def check_Cmusic_name(url, name):
    file_name = name.split('/')[-1]
    file_name = file_name.split('.')[0]
    # 分割文件名以提取艺术家和歌曲名
    artist, song_with_extension = file_name.split(' - ')
    song = song_with_extension.split('_')[0]  # 去掉后缀
    ids = get_id(url)
    data = get_data(ids)
    Cname = data['songs'][0]['name']
    Cname = Current_lry.LRY().remove_parentheses_content(Cname)
    score = Current_lry.LRY().get_right_lry(song, Cname)
    if score > 0.9:
        return True
    else:
        print(f'song:{song}不匹配{Cname}')

        return False
