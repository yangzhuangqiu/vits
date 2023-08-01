import os
import re
from pydub import AudioSegment

# 将音频文件按字幕文件拆分成小文件
def split_audio_by_subtitles(audio_file, subtitle_file, output_dir, prefix):
    # 读取字幕文件并提取每个字幕的开始时间和结束时间
    subtitle_times = []
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        for line in f:
            if re.match(r'^\d+:\d+:\d+,\d+\s-->\s\d+:\d+:\d+,\d+', line):
                start_time_str, end_time_str = line.split('-->')
                start_time = convert_time_str_to_ms(start_time_str.strip())
                end_time = convert_time_str_to_ms(end_time_str.strip())
                subtitle_times.append((start_time, end_time))

    # 使用 PyDub 库加载音频文件
    audio = AudioSegment.from_file(audio_file)

    # 将每个字幕分配到对应的小文件中
    for i, (start_time, end_time) in enumerate(subtitle_times):
        # 根据字幕的开始时间和结束时间，从音频中截取对应的片段
        segment = audio[start_time:end_time]
        # 构造输出文件的路径和文件名
        output_file = os.path.join(output_dir, f'{prefix}_{i+1}.wav')
        # 将音频片段保存为 WAV 文件
        segment.export(output_file, format='wav')


def convert_time_str_to_ms(time_str):
    hours, minutes, seconds_milliseconds = time_str.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    return int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds)


if __name__ == '__main__':
    prefix = 'fy03'
    audio_file = f'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/output/{prefix}.wav'
    subtitle_file = f'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/output/merge_{prefix}.srt'
    output_dir = 'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/output/wavs'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    split_audio_by_subtitles(audio_file, subtitle_file, output_dir, prefix)