import re
import datetime
from datetime import timedelta

# 合并字幕 并 生成训练的文件
def parse_srt(srt_text):
    srt_group = srt_text.strip().split('\n\n')
    parsed_srt = []
    for group in srt_group:
        number, time_range, *text = group.split('\n')
        start_time, end_time = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3})', time_range)
        start_time = timedelta(hours=int(start_time[0:2]), minutes=int(start_time[3:5]),
                               seconds=int(start_time[6:8]), milliseconds=int(start_time[9:]))
        end_time = timedelta(hours=int(end_time[0:2]), minutes=int(end_time[3:5]),
                             seconds=int(end_time[6:8]), milliseconds=int(end_time[9:]))
        parsed_srt.append({'start_time': start_time, 'end_time': end_time, 'text': ' '.join(text)})
    return parsed_srt

def merge_srt(parsed_srt):
    merged_srt = []
    buffer_item = parsed_srt[0]
    for item in parsed_srt[1:]:
        if item['start_time'] - buffer_item['start_time'] < timedelta(seconds=8):
            buffer_item['end_time'] = item['end_time']
            buffer_item['text'] += ' ' + item['text']
        else:
            merged_srt.append(buffer_item)
            buffer_item = item
    merged_srt.append(buffer_item)
    return merged_srt


def timedelta_to_str(timedelta_obj):
    # 将 timedelta 转换成 datetime，并加上一个固定的基准时间
    datetime_obj = datetime.datetime(1900, 1, 1) + timedelta_obj
    # 使用 strftime() 方法将 datetime 格式化成字符串
    return datetime_obj.strftime("%H:%M:%S,%f")[:-3]


def format_srt(merged_srt):
    formatted_srt = ''
    for i, item in enumerate(merged_srt, start=1):
        start_time = timedelta_to_str(item['start_time'])
        end_time = timedelta_to_str(item['end_time'])
        # start_time = str(item['start_time'])
        # end_time = str(item['end_time'])
        # start_time = '0'*(8-len(start_time)) + start_time.replace('.', ',') + '0'*(12-len(start_time))
        # end_time = '0'*(8-len(end_time)) + end_time.replace('.', ',') + '0'*(12-len(end_time))
        formatted_srt += f'{i}\n{start_time} --> {end_time}\n{item["text"]}\n\n'
    return formatted_srt.strip()


def process_srt(srt_text):
    parsed_srt = parse_srt(srt_text)
    merged_srt = merge_srt(parsed_srt)
    return format_srt(merged_srt)


def merge_subtitles(subtitle_file, output_file):
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        srt_text = f.read()

    processed_srt = process_srt(srt_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_srt)


def format_subtitle_file(subtitle_file, prefix, output_file):
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        subtitle_lines = f.readlines()

    formatted_subtitle_lines = []
    count = 0
    for i in range(len(subtitle_lines)):
        line = subtitle_lines[i].strip()
        if line == '':
            continue
        if line.isdigit():
            # 如果当前行是字幕的编号，那么将计数器加 1
            # count += 1
            continue
        elif re.match(r'^\d{2}:\d{2}:\d{2},\d{3}\s-->\s\d{2}:\d{2}:\d{2},\d{3}', line):
            # 如果当前行是字幕的时间戳，那么将计数器加 1
            # count += 1
            continue
        else:
            # 如果当前行是字幕内容，那么将其格式化成对应的字符串
            count += 1
            formatted_line = f"wavs/{prefix}_{count}.wav|{line}"
            formatted_subtitle_lines.append(formatted_line)

    # 将格式化后的字幕内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(formatted_subtitle_lines))


def main():
    # 合并字幕
    prefix = 'fy03'
    subtitle_file = f'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/output/{prefix}.srt'
    output_file = f'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/output/merge_{prefix}.srt'
    merge_subtitles(subtitle_file, output_file)

    train_file = f'C:/Users/yangzhuangqiu/Desktop/tmp/python/convert/output/train_{prefix}.txt'
    format_subtitle_file(output_file, prefix, train_file)


if __name__ == '__main__':
    main()