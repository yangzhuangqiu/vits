import os
import glob
from pydub import AudioSegment

# 将音频文件转成可以训练的文件
def convert_file(input_file, output_file):
    sound = AudioSegment.from_file(input_file)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(22050)
    sound = sound.set_sample_width(2)  # 16-bit PCM is 2 bytes per sample
    sound.export(output_file, format="wav")


def convert_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for input_file in glob.glob(os.path.join(input_dir, '*.wav')):
        output_file = os.path.join(output_dir, os.path.basename(input_file)) # .replace('.m4a', '.wav')
        convert_file(input_file, output_file)


def convert_format():
    input_dir = 'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/input'
    output_dir = 'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/output'

    convert_directory(input_dir, output_dir)
    print(f"Conversion complete for all files in '{input_dir}'")


def main():
    convert_format()


if __name__ == '__main__':
    main()