# -*- coding: utf-8 -*-
import re

from PIL import Image
import shutil
from ncmdump import NeteaseCloudMusicFile
import requests
import urllib.parse

from gradio_client import Client, handle_file
import os
import json
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


def turning(name):
    file_path = os.path.join('music', f"{name}.ncm")
    if os.path.exists(file_path):


        endname = os.path.join('music', f"{name}.mp3")
        ncmfile = NeteaseCloudMusicFile(os.path.join('music', f"{name}.ncm"))
        ncmfile.decrypt()
        print(ncmfile.music_metadata)  # show music metadata

        ncmfile.dump_music(endname)  # auto detect correct suffix
        return name
    else:
        return name

class MSST():
    def depart(self, name):
        client = Client("http://localhost:7860/")
        result = client.predict(
            selected_model='dereverb_mel_band_roformer_less_aggressive_anvuew_sdr_18.8050.ckpt',
            input_audio=[handle_file(f'{name}.mp3')],
            store_dir="results/",
            extract_instrumental=False,
            gpu_id="0",
            output_format="mp3",
            force_cpu=False,
            use_tta=False,
            api_name="/run_inference_single"
        )

        fine_name = f'{name}_noreverb.mp3'.split('\\')[-1]

        path = rf'E:\MSST WebUI\results\{fine_name}'
        target_path = os.path.join(os.getcwd(), fine_name)

        # 移动文件
        shutil.move(path, target_path)

        return fine_name.split('.')[0]


class MSSTF():
    def departF(self, name):
        fine_name = f'{name}_noreverb.mp3'
        target_path = os.path.join(os.getcwd(), fine_name)

        # 检查目标路径是否存在
        if os.path.exists(target_path):
            print(f"文件已存在: {target_path}")
            return fine_name.split('.')[0]

        # 创建 MSST 实例并调用 departF 函数
        m = MSST()
        name_with_path = os.path.join('music', name)
        print(f'正在分离音频 {name_with_path}')

        # 调用 depart 方法
        return m.depart(name_with_path)


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
            print(f'使用缓存的文件: {file_path}')
            # print(eng, cn)
            return eng, cn
    else:
        # 文件不存在，进行网络请求
        url1 = f'https://music.163.com/api/song/media?id={ids}'
        url2 = f'https://music.163.com/api/song/lyric?os=pc&id={ids}&lv=-1&tv=-1'

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


def checking_path(url):
    path = download_pic(get_id(url), get_pic(get_data(get_id(url))))
    path = pic_making.image_main(path)
    return path


def check_Cmusic_name(url, name):
    file_name = name.split('/')[-1]
    file_name=file_name.split('.')[0]
    # 分割文件名以提取艺术家和歌曲名
    artist, song_with_extension = file_name.split(' - ')
    song = song_with_extension.split('_')[0]  # 去掉后缀
    ids = get_id(url)
    data = get_data(ids)
    Cname = data['songs'][0]['name']
    score = Current_lry.LRY().get_right_lry(song, Cname)
    if score > 0.9:
        return True
    else:
        print(f'song:{song}不匹配{Cname}')

        return False


def ncm2mp3main(name):

    name = turning(name)  # ncm2mp3
    # print(name)
    m = MSSTF().departF(name)
    print(m)


if __name__ == '__main__':
    ncm2mp3main('HOYO-MiX - Da Capo')  # 把music文件夹下的ncm转换成mp3然后人声分离把音频放到主目录下
