import shutil

from gradio_client import Client, handle_file
import os

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

        path = rf'E:\MSST WebUI\results\{fine_name}'
        target_path = os.path.join(os.getcwd(), fine_name)

        # 移动文件
        shutil.move(path, target_path)

        return fine_name.split('.')[0]


class MSSTF():
    def departF(self, name):
        m = MSST()
        print(f'正在分离音频{name}')

        return m.depart(name)
