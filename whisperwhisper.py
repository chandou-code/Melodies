# -*- coding: utf-8 -*-

import whisper


class W():
    def transcribe_audio(self, audio_file, model, language=None):
        # 使用 Whisper 进行转录
        result = model.transcribe(audio_file, language=language)
        return result['text']


class WF():
    def translationF(self, audio_file):
        # 加载 Whisper 模型
        w = W()
        # 确保使用 GPU
        device = "cpu"
        model = whisper.load_model("medium", device=device)  # 加载模型到 GPU

        # 示例调用
        transcribed_text = w.transcribe_audio(audio_file, model, 'en')

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
        if len(text) < 5:  # 示例：如果文本长度小于5，认为是无意义的
            return False
        return True

if __name__ == '__main__':
    audio_file = 'temp/TEMP_26.wav'
    wf = WF()
    # print(torch.cuda.is_available())
    transcribed_text = wf.translationF(audio_file)

    print(transcribed_text)

    # import torch
    # print(torch.__version__)  # 检查PyTorch版本
    #
    #
    # print(torch.cuda.is_available())  # true 则开启成功
