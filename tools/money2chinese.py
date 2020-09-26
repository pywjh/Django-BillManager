# -*- coding: utf-8 -*-
# ========================================
# Author: wjh
# Date：2020/9/26
# FILE: money2chinese
# ========================================


def money2chinese(money_number):
    u"""
    .转换数字为大写货币格式
    @:param money_number: 金额(float, int, long, string 且小于15位)
    @:return chinese_str: 大写的金额字符串
    """
    format_word = [u"分", u"角", u"元",
                   u"拾", u"百", u"千", u"万",
                   u"拾", u"百", u"千", u"亿",
                   u"拾", u"百", u"千", u"万",
                   u"拾", u"百", u"千", u"兆"]

    format_num = [u"零", u"壹", u"贰", u"叁", u"肆", u"伍", u"陆", u"柒", u"捌", u"玖"]
    if isinstance(money_number, str):
        # - 如果是字符串,先尝试转换成float或int.
        try:
            if '.' in money_number:
                money_number = float(money_number)
            else:
                money_number = int(money_number)
        except:
            raise ValueError(u'不能识别的字符串：{0}'.format(money_number))
    if isinstance(money_number, float):
        real_numbers = []
        money_len = len(str(money_number))
        for i in range(money_len - 3, -3, -1):
            if money_number >= 10 ** i or i < 1:
                real_numbers.append(int(round(money_number / (10 ** i), 2) % 10))

    elif isinstance(money_number, int):
        real_numbers = [int(i) for i in str(money_number) + '00']

    else:
        raise ValueError(u'非法传参')

    # 标记连续0次数，以删除万字，或适时插入零字
    zflag = 0
    start = len(real_numbers) - 3
    chinese_words = []

    # 使i对应实际位数，负数为角分
    for i in range(start, -3, -1):
        if real_numbers[start - i] or len(chinese_words) == 0:
            if zflag:
                chinese_words.append(format_num[0])
                zflag = 0
            chinese_words.append(format_num[real_numbers[start - i]])
            chinese_words.append(format_word[i + 2])

        # 控制万/元
        elif 0 == i or (0 == i % 4 and zflag < 3):
            chinese_words.append(format_word[i + 2])
            zflag = 0
        else:
            zflag += 1

    if chinese_words[-1] not in (format_word[0], format_word[1]):
        # 最后两位非"角,分"则补"整"
        chinese_words.append("整")

    return ''.join(chinese_words)


if __name__ == '__main__':
    print(money2chinese(float(100.33661)))
