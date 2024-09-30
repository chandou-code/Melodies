# -*- coding: utf-8 -*-
import os.path

from PIL import Image, ImageEnhance, ImageFilter


def resize_and_crop_image(input_path, target_size=(1280, 720)):
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

        # 计算裁剪的起始位置
        left = (new_width - target_width) // 2
        upper = (new_height - target_height) // 2
        right = left + target_width
        lower = upper + target_height

        # 裁剪图片
        cropped_img = resized_img.crop((left, upper, right, lower))

        # 如果是 RGBA 模式，转换为 RGB 模式
        if cropped_img.mode == 'RGBA':
            cropped_img = cropped_img.convert('RGB')

        output_path = f'{input_path.split(".")[0]}_temp.jpg'  # 输出图片路径

        # 保存新的图片
        cropped_img.save(output_path)
        return output_path


def sharpen_image(input_path):
    # 打开图片
    with Image.open(input_path) as img:
        # 锐化图片
        sharpened_img = img.filter(ImageFilter.SHARPEN)

        # 可选：增加对比度
        enhancer = ImageEnhance.Contrast(sharpened_img)
        sharpened_img = enhancer.enhance(1.5)  # 增加对比度，1.0为原始值
        output_path = f'{input_path.split(".")[0]}_finish.jpg'  # 输出图片路径
        # 保存处理后的图片
        sharpened_img.save(output_path)

        return output_path


def image_main(input_image_path):

    temp = os.path.abspath(input_image_path)
    resize = resize_and_crop_image(temp)
    os.remove(temp)
    return sharpen_image(resize)
