# -*- coding: utf-8 -*-
# ========================================
# Author: wjh
# Date：2021/1/9
# FILE: tool
# ========================================
def get_total_earnings(earnings: list) -> list:
    """
    将每日起伏的数据做成汇总列表
    >>> earnings = [1, 2, 3, 4, 5]
    >>> return [1, 3, 6, 10, 15]
    """
    total_earnings_list = []
    tool_num = 0
    for earning in earnings:
        tool_num += earning
        total_earnings_list.append(tool_num)
    return list(map(lambda f: round(f, 3), total_earnings_list))
