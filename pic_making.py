# -*- coding: utf-8 -*-
import os.path
import random
import time
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


# def crop_image_to_9_16(input_path):
#     print(input_path)
#     # 打开图片
#     with Image.open(input_path) as img:
#         width, height = img.size
#
#         # 计算目标尺寸
#         target_height = height
#         target_width = (9 * target_height) // 16
#
#         if width > target_width:
#             # 如果原图宽度大于目标宽度，计算裁剪的边界
#             left = (width - target_width) // 2
#             right = (width + target_width) // 2
#             img_cropped = img.crop((left, 0, right, target_height))
#         else:
#             # 否则，按照宽度裁剪
#             target_width = width
#             target_height = (16 * target_width) // 9
#             top = (height - target_height) // 2
#             bottom = (height + target_height) // 2
#             img_cropped = img.crop((0, top, target_width, bottom))
#
#         # 保存裁剪后的图片
#         input_path = input_path.split('\\')[-1]
#         output_path = os.path.join('cover_output', f'{input_path.split(".")[0]}_temp.jpg')
#
#         img_cropped.save(output_path)
#         return output_path

# 使用示例

def crop_image_content(input_path,target_size):
        # print(input_path)
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

            output_path = os.path.join('cover_output', f'{os.path.basename(input_path)}')
            # output_path = os.path.join('cover_output', f'{input_path.split("/")[-1].split(".")[0]}{time.time()}.jpg')

            # 保存新的图片
            cropped_img.save(output_path)
            return output_path


def crop_image_cover(input_path, target_size):
    # print(input_path)
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

        output_path = os.path.join('cover_output', f'{os.path.basename(input_path)}')

        # 保存新的图片
        cropped_img.save(output_path)
        return output_path

def sharpen_image(input_path):
    # 打开图片
    with Image.open(input_path) as img:
        original_size = img.size

        img_width, img_height = original_size
        target_width, target_height = (1280, 720)
        # 锐化图片
        sharpened_img = img.filter(ImageFilter.SHARPEN)

        # 可选：增加对比度
        enhancer = ImageEnhance.Contrast(sharpened_img)
        sharpened_img = enhancer.enhance(1.5)  # 增加对比度，1.0为原始值
        output_path = f'{input_path.split(".")[0]}_finish.jpg'  # 输出图片路径
        # 保存处理后的图片
        sharpened_img.save(output_path)

        return output_path






# from PIL import Image

# print(crop_image_to_16_9_top_center('4DDBED10B9605A3CD41543B2AF16EEBD.jpg', '4DDBED10B9605A3CD41543B2AF16EEBD_t.jpg'))
