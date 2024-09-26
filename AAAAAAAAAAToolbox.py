# -*- coding: utf-8 -*-
import re

from PIL import Image
import shutil

import requests
import urllib.parse

from gradio_client import Client, handle_file
import os


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
    from ncmdump import NeteaseCloudMusicFile
    ncmfile = NeteaseCloudMusicFile(f"./{name}.ncm")
    ncmfile.decrypt()

    print(ncmfile.music_metadata)  # show music metadata

    ncmfile.dump_music(f"./{name}.mp3")  # auto detect correct suffix
    return f"{name}"


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
        fine_name = f'{name}_noreverb.mp3'
        print(fine_name)
        path = rf'E:\MSST WebUI\results\{fine_name}'
        target_path = os.path.join(os.getcwd(), fine_name)

        # 移动文件
        shutil.move(path, target_path)

        return fine_name.split('.')[0]


class MSSTF():
    def departF(self, name):
        m = MSST()
        print(f'正在分离音频{name}')
        # os.remove(f'{name}.mp3')
        # os.remove(f'{name}.ncm')
        return m.depart(name)


def get_pic(ids):
    url = f'https://music.163.com/api/song/detail?ids=[{ids}]'
    r = requests.get(url)
    u = r.json()["songs"][0]["album"]["blurPicUrl"]
    print(u)
    return u


def download_pic(name, url):
    # 本地保存的文件名
    file_name = f"{name}.jpg"

    # 发送请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 保存图片到本地
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"图片已保存为 {file_name}")
    else:
        print("下载图片失败")


def download_lyr(ids):
    url1 = f'https://music.163.com/api/song/media?id={ids}'
    url2 = f'https://music.163.com/api/song/lyric?os=pc&id={ids}&lv=-1&tv=-1'
    r = requests.get(url1)
    eng = r.json()['lyric']
    r = requests.get(url2)
    cn = r.json()['tlyric']['lyric']

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


if __name__ == '__main__':
    url = 'https://music.163.com/song?id=1813960297&userid=129707286'

    # download_pic(get_id(url), get_pic(get_id(url)))
    # eng = "[00:00.130]Lately, I've been, I've been losing sleep\n[00:04.990]Dreaming about the things that we could be\n[00:09.030]But baby, I've been, I've been praying hard,\n[00:13.320]Said no more counting dollars\n[00:15.870]We'll be counting stars, yeah we'll be counting stars\n[00:24.630]\n[00:37.580]I see this life like a swinging vine\n[00:40.160]Swing my heart across the line\n[00:41.990]And my face is flashing signs\n[00:44.300]Seek it out and you shall find\n[00:46.120]Old, but I'm not that old\n[00:48.170]Young, but I'm not that bold\n[00:50.000]I don't think the world is sold\n[00:51.760]On just doing what we're told\n[00:54.250]I~ feel something so right\n[00:58.720]Doing the wrong thing\n[01:01.710]I~ feel something so wrong\n[01:06.470]Doing the right thing\n[01:10.060]I could lie, could lie, could lie\n[01:13.050]Everything that kills me makes me feel alive\n[01:17.730]\n[01:17.950]Lately, I've been, I've been losing sleep\n[01:21.460]Dreaming about the things that we could be\n[01:25.450]But baby, I've been, I've been praying hard,\n[01:29.300]Said, no more counting dollars\n[01:31.450]We'll be counting stars\n[01:32.950]\n[01:33.290]Lately, I've been, I've been losing sleep\n[01:37.080]Dreaming about the things that we could be\n[01:40.770]But baby, I've been, I've been praying hard,\n[01:44.960]Said, no more counting dollars\n[01:47.140]We'll be, we'll be counting stars\n[01:50.290]\n[01:56.290]I feel the love and I feel it burn\n[01:58.710]Down this river, every turn\n[02:00.710]Hope is our four-letter word\n[02:02.620]Make that money, watch it burn\n[02:04.870]Old，but I'm not that old\n[02:06.750]Young, but I'm not that bold\n[02:08.720]I don't think the world is sold\n[02:10.990]On just doing what we're told\n[02:12.770]I~ feel something so wrong\n[02:17.250]By Doing the right thing\n[02:20.680]I could lie, could lie, could lie\n[02:24.470]Everything that drowns me makes me wanna fly\n[02:28.540]\n[02:28.790]Lately, I've been, I've been losing sleep\n[02:32.180]Dreaming about the things that we could be\n[02:35.930]But baby, I've been, I've been praying hard,\n[02:40.030]Said  no more counting dollars\n[02:42.310]We'll be counting stars\n[02:43.810]\n[02:44.030]Lately, I've been, I've been losing sleep\n[02:47.800]Dreaming about the things that we could be\n[02:51.600]But baby, I've been, I've been praying hard,\n[02:56.000]Said, no more counting dollars\n[02:58.040]We'll be, we'll be counting stars\n[03:00.840]\n[03:04.120]Take that money\n[03:04.630]Watch it burn\n[03:05.630]Sink in the river\n[03:06.710]The lessons I've learned\n[03:07.440]\n[03:07.730]Take that money\n[03:08.320]Watch it burn\n[03:09.440]Sink in the river\n[03:10.550]The lessons I've learned\n[03:11.380]\n[03:11.660]Take that money\n[03:12.610]Watch it burn\n[03:13.520]Sink in the river\n[03:14.430]The lessons I've learned\n[03:15.320]\n[03:15.600]Take that money\n[03:16.610]Watch it burn\n[03:17.480]Sink in the river\n[03:18.450]The lessons I've learned\n[03:19.160]\n[03:19.500]Everything that kills me makes me feel alive\n[03:26.700]\n[03:26.790]Lately, I've been, I've been losing sleep\n[03:30.150]Dreaming about the things that we could be\n[03:33.890]But baby, I've been, I've been praying hard,\n[03:38.170]Said, no more counting dollars\n[03:40.190]We'll be counting stars\n[03:41.610]\n[03:41.910]Lately, I've been, I've been losing sleep\n[03:45.520]Dreaming about the things that we could be\n[03:49.720]But baby, I've been, I've been praying hard,\n[03:53.900]Said, no more counting dollars\n[03:55.980]We'll be, we'll be, counting stars\n[03:57.910]\n[03:58.090]Take that money\n[03:58.860]Watch it burn\n[03:59.750]Sink in the river\n[04:00.740]The lessons I've learned\n[04:01.440]\n[04:01.840]Take that money\n[04:02.790]Watch it burn\n[04:03.770]Sink in the river\n[04:04.680]The lessons I've learned\n[04:05.430]\n[04:05.790]Take that money\n[04:06.750]Watch it burn\n[04:07.620]Sink in the river\n[04:08.520]The lessons I've learned\n[04:09.290]\n[04:09.660]Take that money\n[04:10.700]Watch it burn\n[04:11.690]Sink in the river\n[04:12.610]The lessons I've learned\n[04:13.690]"

    # eng, cn = download_lyr(get_id(url))




    # pict('28575553.jpg')

    name = 'Carly Rae Jepsen - Call Me Maybe'
    name = turning(name)  # ncm2mp3
    print(name)
    m = MSSTF().departF(name)
