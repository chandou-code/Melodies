# -*- coding: utf-8 -*-
import os

from moviepy.editor import VideoFileClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


# 创建文本图像
def create_text_image(text,size):
    font = ImageFont.truetype("QingNiaoHuaGuangJianMeiHei-2.ttf", size)
    image = Image.new('RGBA', (800, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font, fill='white')
    return image


def add_text2video(inputfile, music_name1):
    text_image1 = create_text_image("英语歌词磨听力开源",80)

    text_image2 = create_text_image(f"BGM:{music_name1.split('-')[-1].split('_')[0]}",40)

    text_image1.save("temp/text_image1.png")
    text_image2.save("temp/text_image2.png")

    # 加载视频
    video = VideoFileClip(inputfile)

    # 创建文本剪辑，分别设置不同位置

    # 创建文本剪辑
    text_clip1 = ImageClip("temp/text_image1.png").set_duration(video.duration).set_position(("center", "top"))
    text_clip2 = ImageClip("temp/text_image2.png").set_duration(video.duration)

    # 获取 text_clip1 的高度
    text_height1 = text_clip1.size[1]

    # 设置 text_clip2 位置为 text_clip1 的底部加上间距
    padding = 10  # 设定间距
    text_clip2 = text_clip2.set_position(("center", text_height1 + padding)).set_duration(video.duration)
    # 合成视频
    final_video = CompositeVideoClip([video, text_clip1, text_clip2])

    codec = video.codec if hasattr(video, 'codec') else 'libx264'
    audio = video.audio

    final_video.set_audio(audio)  # 添加音频

    # 修改输出文件名
    base, ext = os.path.splitext(inputfile)  # 分离文件名和扩展名
    outputfile = f"{base}_output{ext}"  # 新的输出文件名

    final_video.write_videofile(outputfile, codec=codec, audio_codec='aac')

    return outputfile  # 返回新的输出文件名


if __name__ == '__main__':
    add_text2video("Anson Seabra - Keep Your Head Up Princess_bili.mp4")
