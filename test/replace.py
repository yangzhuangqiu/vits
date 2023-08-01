def replace_comma_and_period(text):
    text = text.replace("，", " ").replace("。", " 。 ").replace("：", " ").replace("？", "  ")
    return text

if __name__ == "__main__":
    # 多行文本示例
    text = """
    """

    # 调用函数进行替换
    text = replace_comma_and_period(text)
    print(text)