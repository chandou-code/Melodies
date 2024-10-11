# API调用代码
import os
import random
import shutil
import time

import requests


class TTS():


    def text2speak(self, text):
        voice = random.choice([2222, 3333])
        res = requests.post('http://127.0.0.1:9966/tts', data={
            "text": f"{text}",
            "prompt": "",
            "voice":  str(voice),
            "temperature": 0.3,
            "top_p": 0.7,
            "top_k": 20,
            "refine_max_new_token": "384",
            "infer_max_new_token": "2048",
            "skip_refine": 0,
            "is_split": 1,
            "custom_voice": 0
        })

        return res.json()['audio_files'][0]['filename']


class TTSF():
    def text2speakF(self, text,p):
        t = TTS()
        path = f'temp'
        full_path = os.path.join(path, f'V{int(time.time())}_{p}.wav')
        shutil.move(t.text2speak(text), full_path)
        return full_path

# {code:0, msg:'ok', audio_files:[{filename: E:/ChatTTS-UI-0.84/static/wavs/215144_use3.13s-audio2.21s-seed5099-te0.3-tp0.7-tk20-textlen8-81768.wav, url: http://127.0.0.1:9966/static/wavs/215144_use3.13s-audio2.21s-seed5099-te0.3-tp0.7-tk20-textlen8-81768.wav}]}
#
# #error
# {code:1, msg:"error"}
