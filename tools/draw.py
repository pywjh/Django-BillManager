from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, WordCloud


def draw_balance_bar(xaxis, yaxis, difference=None, title="消费统计", markline=None, width=2000) -> Bar:
    """
    x = [月_日, 月_日, 月_日, ....]
    y = [(title1, [num1, num2, num3, num4, ...]), (title2, [num1, num2, num3, num4, ...])]
    :param difference: 差值 (比如：收入100，消费80，差值就是20) : ['title', [1,2,3,4]]
    :param xaxis: x轴
    :param yaxis: y轴
    :param title: 标题
    :param markline: 标记辅助线
    :param width: 宽
    :return: Bar
    """
    bar = Bar()
    bar.add_xaxis(xaxis)
    for name, axis in yaxis:
        bar.add_yaxis(name, axis, category_gap="20%", gap="0%")
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title, ),
                        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100),
                                       opts.DataZoomOpts(type_="inside")],
                        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'))
    bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    if difference:
        name, diff_yaxis = difference
        line = Line().add_xaxis(xaxis).add_yaxis(
            name,
            diff_yaxis,
            symbol_size=15,
            z_level=1,
            is_symbol_show=False,
        )
        bar.overlap(line)

    if markline is not None:
        bar.set_series_opts(markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(
                y=markline,
                name='预算')
            ])
        )

    return bar


def draw_balance_line(xaxis, yaxis, title="消费统计", markline=None, width=2000) -> Line:
    """
        x = [月_日, 月_日, 月_日, ....]
        y = [(title1, [num1, num2, num3, num4, ...]), (title2, [num1, num2, num3, num4, ...])]
        :param xaxis: x轴
        :param yaxis: y轴
        :param title: 标题
        :param markline: 标记辅助线
        :param width: 宽
        :return: Line
        """
    line = Line()
    line.add_xaxis(xaxis)
    for name, axis in yaxis:
        line.add_yaxis(name, axis, is_symbol_show=True)
    line.set_global_opts(title_opts=opts.TitleOpts(title=title, ),
                        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100),
                                       opts.DataZoomOpts(type_="inside")],
                        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'))
    line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    if markline is not None:
        line.set_series_opts(markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(
                y=markline,
                name='预算')
            ])
        )

    return line


def draw_usage_pie(payout, budget, title) -> Pie:
    """
    list [(title1, num1), (title2, num2)]
    :param payout: 消费
    :param budget: 预算
    :param title:  标题
    :return: Pie
    """
    pie = Pie()
    pie.add(series_name=title,
          data_pair=budget,
          radius=["0%", "40%"],
          label_opts=opts.LabelOpts(position="inner"),
          )
    pie.add(series_name=title,
          radius=["40%", "50%"],
          data_pair=payout,
          label_opts=opts.LabelOpts(position="outside",
                                    formatter="{b}:\n{c}({d}%)",
                                    border_width=1,
                                    border_radius=4,
                                    ),
          )

    # pie.set_global_opts(
    #     legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"), )
    # pie.set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item",
    #                                                 formatter="{a} <br/>{b}: {c} ({d}%)"))

    return pie


def draw_category_pie(inner, outside, inner_title="分类报表", outer_title='小类报表', width=2000) -> Pie:
    pie = Pie()

    inner_radius = "70%"
    outer_radius = "80%"

    pie.add(series_name=inner_title,
          data_pair=inner,
          radius=["0%", inner_radius],
          label_opts=opts.LabelOpts(position="inner"),
          )
    pie.add(series_name=outer_title,
          radius=[inner_radius, outer_radius],
          data_pair=outside,
          label_opts=opts.LabelOpts(position="outside",
                                    formatter="{b}:\n{c}({d}%)",
                                    border_width=1,
                                    border_radius=4,
                                    ),
          )

    pie.set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"), )
    pie.set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"))

    return pie


def draw_wordcloud(data: list, title: str = '云词分析') -> WordCloud:
    """
    生成云图
    data: list(tuple(name1, number1), tuple(name2, number2))
    """
    wd: WordCloud = WordCloud()
    wd.add(series_name=title, data_pair=data, word_size_range=[15, 80]).set_global_opts(
        title_opts=opts.TitleOpts(
            title=title, title_textstyle_opts=opts.TextStyleOpts(font_size=40)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    return wd