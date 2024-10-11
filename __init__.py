# -*- coding: utf-8 -*-
import os
import translation
import ChatTTS
import split_audio
import whisperwhisper
import new_audio
import Current_lry
import search
import Toolbox
import cover_making
import pic_making
import add_content
import Cutting_audio
import clear_temp

def main():
    dur = 200
    background='content_pic/109951166421319018.jpg'
    pres = search.main()
    for pre in pres:
        if not pre['Flag']:
            continue
        music_name1, url = pre['name'], pre['Curl']
        music_name = Toolbox.MSSTF().departF(music_name1)
        if not Toolbox.check_Cmusic_name(url, music_name):
            continue
        tks = Cutting_audio.main_main(url, music_name)
        pic_path_tiktok_ = pic_making.crop_image_cover(cover_making.get_random_cover('dy'), (1080, 1920))
        pic_path_bili_ = pic_making.crop_image_cover(cover_making.get_random_cover('b'), (1280, 720))
        pic_path_tiktok = pic_making.crop_image_content(background, (1080, 1920))
        pic_path_bili = pic_making.crop_image_content(background, (1280, 720))
        index = 0
        while index < len(tks):
            file_name_without_ext = os.path.splitext(os.path.basename(tks[index]['path']))[0]  # 获取文件名不含扩展名
            tks[index]['text'], tks[index]['CNtext'] = Current_lry.LRYf().lryF(url, tks[index])
            tks[index]['AItextPath'] = ChatTTS.TTSF().text2speakF(tks[index]['CNtext'], file_name_without_ext)
            tks[index]['middlePath'] = new_audio.control_audioF().combined_Mp3(
                tks[index]['AItextPath'],
                tks[index]['path'],
                file_name_without_ext, dur)
            tks[index]['tiktokMp4'], tks[index]['biliMp4'], = new_audio.control_audioF().combined_all_wav2mp4(
                tks[index], file_name_without_ext, dur, pic_path_tiktok, pic_path_bili)
            index += 1
        bili, tik = new_audio.control_audioF().make_videos(tks, music_name1, pic_path_tiktok_, pic_path_bili_)
        new_audio.control_audio().all_temp(tks)
        clear_temp.clearing()
if __name__ == '__main__':
    main()
