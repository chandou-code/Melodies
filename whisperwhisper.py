# -*- coding: utf-8 -*-
import os.path

import whisper


class W():
    def transcribe_audio(self, audio_file):
        from faster_whisper import WhisperModel

        model_size = "medium"

        # Run on GPU with FP16
        # model = WhisperModel(model_size, device="cuda", compute_type="float16")

        # or run on GPU with INT8
        # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
        # or run on CPU with INT8
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

        segments, info = model.transcribe(os.path.abspath(audio_file), beam_size=5)

        # print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        text = ''
        for segment in segments:
            # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            text += segment.text
        try:
            print(text)
        except Exception as e:
            print(f"语言检测错误: {e}")
            text = ''
        return text


class WF():
    def translationF(self, audio_file):
        # 加载 Whisper 模型
        transcribed_text = W().transcribe_audio(audio_file)

        # 判断转录文本是否有效
        if self.is_meaningful(transcribed_text):
            return transcribed_text.strip()  # 返回去掉空格的文本
        else:
            return None  # 或者返回一个特定的消息，例如 "无意义音频"

    def is_meaningful(self, text):
        # 检查文本是否为空或仅包含空格
        if not text or text.strip() == "":
            return False
        # 可以添加更多逻辑来判断文本内容是否有意义
        # 例如：检查文本长度、是否包含特定关键词等
        if len(text) < 4:  # 示例：如果文本长度小于5，认为是无意义的
            return False
        return True


if __name__ == '__main__':
    # import torch
    #
    # print(torch.version.cuda)  # 输出CUDA版本

    print(WF().translationF('temp/TEMP_4.wav'))
    # print(whisper.__file__)
#
