# -*- coding: utf-8 -*-
import difflib
import os.path
from collections import Counter

import requests
import Toolbox
from pathlib import Path
import Current_lry


def get_id_by_name(name):
    url = f'https://music.163.com/api/search/get?s={name}&type=1&offset=0&limit=1'
    # print(url)
    r = requests.get(url)

    # 使用 .get() 方法来避免 KeyError
    songs = r.json().get("result", {}).get("songs")

    if songs:
        Curl = f'https://music.163.com/song?id={songs[0]["id"]}'
        return name, Curl, True
    return name, 0, False


def is_korean(text):
    return any('\uAC00' <= char <= '\uD7A3' for char in text)  # 韩文字符范围


def is_chinese(text):
    return any('\u4E00' <= char <= '\u9FFF' for char in text)  # 中文字符范围


def remove_if_similar(item_list):
    # 用于存储最终结果
    unique_texts = []

    for item in item_list:
        text_to_check = item['text']
        is_similar = False

        for unique_item in unique_texts:
            if get_right_lry(text_to_check, unique_item['text']) > 0.85:
                is_similar = True
                break

        if not is_similar:
            unique_texts.append(item)

    return unique_texts


def pre_(url, name):
    # try:
    eng, cn = Toolbox.download_lyr(Toolbox.get_id(url))
    # print(cn)

    tt = Current_lry.LRY().lry(eng, cn)
    print('tt', url, name, tt)
    tt = remove_if_similar(tt)
    texts = [item['text'] for item in tt]

    # 使用 Counter 统计次数

    # print('tt', name, tt)
    # except UnicodeEncodeError:
    #     return False, 1  # 返回 False 以表示发生了错误

    if not tt:  # 判断是否存在英文歌词
        print('if not tt')
        return False, 1
    if not cn:  # 判断是否存在中文歌词
        print('if not cn')
        return False, 1

    text_counts = Counter(texts)
    most_common = text_counts.most_common(1)  # 1 表示只获取最高频率的元素
    highest_text, highest_count = most_common[0]  # 提取文本和次数
    with open('output.txt', 'a',encoding='utf-8') as f:  # 'a' 表示追加模式
        f.write(f"{name} | {highest_text} | {highest_count}\n")

    # if highest_count > 5:  # 一句话出现频率过高
    #     return False, 1

    count_count = 0
    words_count = 0
    for t in tt:
        text = t['text']
        # print('text', text)
        word_count_c = len(text.split())
        # print('word_count_c', word_count_c)
        word_count = Counter(text.split())

        # 计算重复单词的个数
        repeated_count = sum(1 for count in word_count.values() if count > 1)

        # print('before', text, word_count)
        if word_count_c < 4:  # 初步判断，要求每句的歌词不能过短 短歌词比例不能超过百分之???
            # count_count += 0.3
            count_count += 1
            # print(text)
            continue
        if any(word in text for word in ['Yeah', 'haha', 'yeah', 'oh', 'OH', 'Oh']):
            # print(text)
            # words_count += 0.8
            words_count += 1
            continue
        # if '作曲' in text:
        #     print(text)
        #     count_count += 1000
        #     continue
        # if ':' in text:
        #     print(text)
        #     count_count += 1000
        #     continue
        # if '：' in text:
        #     print(text)
        #     count_count += 1000
        #     continue

    # print(count)
    ratio = (count_count + words_count) / len(tt)  # 直接除法会得到浮点数
    # print(name,'count_count:', count_count, 'words_count:', words_count, 'count_count + words_count:', count_count + words_count, 'ratio:', ratio,
    #       'len(tt):', len(tt))
    output_file = 'pres.txt'
    with open(output_file, 'a') as f:
        f.write(f"{name}, count_count: {count_count}, words_count: {words_count}, "
                f"count_count + words_count: {count_count + words_count}, ratio: {ratio}, "
                f"len(tt): {len(tt)}\n")
    # print(f"{name}符合条件的句子比例:", ratio)

    return ratio < 0.25, ratio
    # return True, ratio


def transform_string(input_str):
    # 移除逗号和空格
    return input_str.replace(',', '').replace('$', '').replace(r"'", '').replace('(', '').replace(')', '')


def main():
    directory = Path('music')
    # 用于存储唯一前缀的集合
    for f in directory.iterdir():
        if f.is_file():
            # 获取不带扩展名的文件名
            new_name = transform_string(f.name.split('.')[0])
            # 获取文件的扩展名
            extension = f.suffix

            # 创建新的文件名
            new_file_name = f.parent / f"{new_name}{extension}"

            # 重命名文件
            f.rename(new_file_name)

    unique_prefixes = set()
    file_names = []

    for f in directory.iterdir():
        if f.is_file():
            prefix = transform_string(f.name.split('.')[0].split('_')[0])
            # 检查前缀是否已经存在
            if prefix not in unique_prefixes:
                unique_prefixes.add(prefix)
                file_names.append({"name": prefix})
    # file_names = [{
    #     "name": "Westlife - Soledad"
    # }]

    pres = []
    for file in file_names:
        name, Curl, f = get_id_by_name(file['name'])
        if not f:  # 首先过滤纯音乐/没有歌词的音乐
            print('if not f')
            file['Flag'] = False
            file['Curl'] = Curl
            file['score'] = 1

            pres.append(file)
            continue

        file['Flag'], file['score'] = pre_(Curl, name)
        file['Curl'] = Curl

        pres.append(file)
    print('pres',pres)
    return pres


def get_right_lry(text1, text2):
    similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    return float(f'{similarity:.2f}')


if __name__ == '__main__':
    # 指定目录
    # print(main())

    # if any(word in text for word in ['Yeah', 'haha']):
    #     print(text)
    def remove_duplicates(result1):
        seen_texts = set()  # 用于存储已见过的 text
        unique_result = []  # 存储唯一的结果

        for item in result1:
            text = item['text']
            if text not in seen_texts:
                seen_texts.add(text)  # 添加到集合中
                unique_result.append(item)  # 保留这个字典项

        return unique_result


    # 示例输入
    result1 = [
        {"text": "Hello", "id": 1},
        {"text": "World", "id": 2},
        {"text": "Hello", "id": 3},
        {"text": "Python", "id": 4},
        {"text": "World", "id": 5}
    ]

    # 调用函数
    unique_results = remove_duplicates(result1)

    # 打印输出
    print(unique_results)
