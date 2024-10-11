# -*- coding: utf-8 -*-
import os.path
import subprocess
import time
import ffmpeg
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageEnhance, ImageFilter
import random
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.VideoClip import ImageClip

from myproject.musics.new_audio import control_audio
import pic_making


def resize_and_crop_image(input_path, target_size=(960, 720)):
    # 打开图片
    with Image.open(input_path) as img:
        img_width, img_height = img.size
        target_width, target_height = target_size

        # 计算放大比例
        width_ratio = target_width / img_width
        height_ratio = target_height / img_height
        scale_ratio = max(width_ratio, height_ratio)

        # 计算放大后的新尺寸
        new_width = int(img_width * scale_ratio)
        new_height = int(img_height * scale_ratio)

        # 放大图片
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

        # 计算裁剪的起始位置（从顶部开始裁剪）
        left = (new_width - target_width) // 2
        upper = 0  # 从顶部开始裁剪
        right = left + target_width
        lower = upper + target_height

        # 确保裁剪区域不超出图像边界
        if lower > new_height:
            lower = new_height
            upper = lower - target_height

        # 裁剪图片
        cropped_img = resized_img.crop((left, upper, right, lower))

        # 如果是 RGBA 模式，转换为 RGB 模式
        if cropped_img.mode == 'RGBA':
            cropped_img = cropped_img.convert('RGB')

        output_path = os.path.join('cover_output', 'temp.jpg')

        # 保存新的图片
        cropped_img.save(output_path)
        return output_path


def random_font_size(min_size=20, max_size=60):
    """生成一个随机的字体大小"""
    return random.randint(min_size, max_size)


def random_color():
    """生成一个随机的 RGB 颜色"""
    color_type = random.choice(['dark_blue', 'dark_green', 'dark_black'])

    if color_type == 'dark_blue':
        return (random.randint(0, 50), random.randint(0, 50), random.randint(100, 255))  # 蓝色通道高
    elif color_type == 'dark_green':
        return (random.randint(0, 50), random.randint(100, 255), random.randint(0, 50))  # 绿色通道高
    elif color_type == 'dark_black':
        # 接近黑色的颜色，R、G、B值都小于 50
        return (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))


def random_position(min_size=30, max_size=60):
    """生成一个随机的字体大小"""
    return random.randint(min_size, max_size)


def calculate_font_size():
    """ 根据图片尺寸动态计算字体大小 """

    return random.randint(80, 100)


def add_chinese_text_to_image(input_image_path, texts):
    # 打开图片
    with Image.open(input_image_path) as img:
        draw = ImageDraw.Draw(img)

        # 获取图片的宽度和高度
        img_width, img_height = img.size

        # 定义相对位置，使用比例
        positions = [
            (img_width * 0.5, img_height * 0.1),  # 上中
            (img_width * 0.5, img_height * 0.4),  # 下中
            (img_width * 0.5, img_height * 0.7),  # 左中
            (img_width * 0.5, img_height * 0.9),  # 右中
        ]

        # 添加四个文本
        for i, text in enumerate(texts):
            font_size = calculate_font_size()  # 动态计算字体大小
            font = ImageFont.truetype("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size)
            color = random_color()  # 生成随机颜色

            # 使用 textbbox 计算文本的边界框
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 在位置上偏移文本的中心
            x = positions[i][0] - text_width / 2
            y = positions[i][1] - text_height / 2

            draw.text((x, y), text, font=font, fill=color)  # 使用随机颜色和大小添加文本

        output_image_path = os.path.join('cover_output', f'{int(time.time())}.jpg')

        img.save(output_image_path)
        os.remove(input_image_path)
        return output_image_path


def get_random_cover(mode):
    directory = ''

    if mode == 'dy':
        directory = Path('cover_tk')
    elif mode == 'b':
        directory = Path('cover_b')

    # 检查目录是否存在
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"目录 '{directory}' 不存在")

    # 获取所有文件名
    file_paths = [str(f) for f in directory.iterdir() if f.is_file()]

    # 检查是否找到了文件
    if not file_paths:
        raise FileNotFoundError(f"在目录 '{directory}' 中未找到任何文件")

    # 随机选择文件
    file_path = random.sample(file_paths, 1)[0]
    return os.path.abspath(file_path)


def main(mode, file_path):
    items = [
        "日常磨耳朵专用",
        "反复磨耳朵",
        "本地部署",
        "英语四六级听力",
        "每天五分钟",
        "坚持磨耳朵",
        "音乐学习法",
        "歌词学习",
        "AI驱动",
        "英文歌曲"

    ]
    items1 = [

        "歌词越听越清楚",
        "将歌词变为学习工具",
        "重塑磨听力学法",
        "高效英语学习",
        "音乐与学习的完美结合",
        "将英文歌曲融入学习新方式",
        "让歌词成为语言学习的桥梁",
        "歌词学习，乐趣与知识双丰收",
        "用旋律激发英语学习热情",
        "让歌词成为语言学习的桥梁",
        "沉浸在音乐中，增强听力技巧",
        "将歌词转化为有效的学习工具",
    ]

    selected_items = random.sample(items, 2)
    selected_items1 = random.sample(items1, 2)
    result = selected_items + selected_items1
    # result = selected_items

    if mode == "dy":
        size_path = pic_making.crop_image_cover(file_path,(1080, 1920))
        fina_path = add_chinese_text_to_image(size_path, result)
        return os.path.abspath(fina_path)
    if mode == "b":
        size_path = pic_making.crop_image_cover(file_path,(1280, 720))
        fina_path = add_chinese_text_to_image(size_path, result)
        return os.path.abspath(fina_path)


def get_image_resolution(pic_file):
    with Image.open(pic_file) as img:
        return img.size  # 返回 (宽度, 高度)


def create_audio_movie(B, M):
    file = os.path.abspath(os.path.join('temp', f'S{int(time.time())}_cover.mp4'))
    command = [
        'ffmpeg',
        '-i', B,
        '-i', M,
        '-y',  # 自动覆盖文件
        '-ar', '44100',  # 设置音频采样率为 44100 Hz
        # '-b:a', '106721b',  # 设置音频比特率为 106721 bps
        file
    ]
    subprocess.run(command)
    return file


def create_background(pic):
    resolution = get_image_resolution(pic)
    file = os.path.abspath(os.path.join('temp', f'Cover_{int(time.time())}.mp4'))
    pic_file = os.path.abspath(pic)

    clip = ImageClip(pic_file).set_duration(0.1)

    clip = clip.resize(newsize=resolution)

    output_path = file
    clip.write_videofile(output_path, fps=6)
    file = create_audio_movie("resource/蔡徐坤鸡叫_爱给网_aigei_com.mp3", file)
    return file


# def unify_video_encoding(video_path, target_resolution):
#     target_fps = 2
#     target_codec = 'libxvid'
#     clip = VideoFileClip(video_path)
#     # 调整分辨率和帧率
#     clip = clip.resize(target_resolution).set_fps(target_fps)
#     # 输出为临时文件
#     output_path = video_path.replace(".mp4", "_converted.mp4")
#     clip.write_videofile(output_path, codec=target_codec, preset='ultrafast', bitrate='500k')
#     # os.remove(output_path)
#     return output_path


def merge_videos(video1, video2, mode):
    if mode == 'b':

        file = os.path.join(f'finish_bili', video2.split('\\')[-1].split('.')[0] + mode + '.mp4')
        clip1 = VideoFileClip(video1)
        clip2 = VideoFileClip(video2)
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.write_videofile(file)
        # os.remove(video1)
        # os.remove(video2)
        return file
    elif mode == 'dy':
        print('执行merge_videos')
        file = os.path.join(f'finish_dy', video2.split('\\')[-1].split('.')[0] + mode + '.mp4')
        clip1 = VideoFileClip(video1)
        clip2 = VideoFileClip(video2)
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.write_videofile(file)
        # os.remove(video1)
        # os.remove(video2)
        return file
    else:
        file = os.path.join(f'finsh', video2.split('\\')[-1].split('.')[0] + mode + '.mp4')
        clip1 = VideoFileClip(video1)
        clip2 = VideoFileClip(video2)
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.write_videofile(file)
        os.remove(video1)
        os.remove(video2)
        return file

    # video2 = os.path.abspath('finsh/Passenger - The Way That I Love You.mp4')
    # mode = 'dy'
    # print(merge_videos(create_background(main("dy")), video2, mode))

    # print(
    #     merge_videos(create_background(main("dy")), 'finsh\Anson Seabra - Keep Your Head Up Princess_tiktok.mp4', 'dy'))
if __name__ == '__main__':
    files='cover_tk/C2EEC43863CAD0FA55AB34E0D234B5FC.jpg'
    print(create_background(files))