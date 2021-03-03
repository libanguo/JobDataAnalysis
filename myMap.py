import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie


class MyMap:

    def __init__(self, frequency):
        self.frequency = frequency  # 设置刷新频率
        self.data = []
        self.count = 0  # 自增，每次add_data后加一
        self.maxNum = 30000
        self.minNum = 0

    def add_data(self, new_item):  # new_item为二维数组
        self.data.append(new_item)
        self.count = self.count + 1
        if self.count % self.frequency == 0:
            self.refresh()

    def get_year_chart(self, number):
        map_data = [
            [x[0], x[1]] for x in self.data[number]
        ]
        min_data, max_data = (self.minNum, self.maxNum)

        map_chart = (
            Map()
                .add(
                series_name="",
                data_pair=map_data,
                zoom=1,
                center=[119.5, 34.5],
                is_map_symbol_show=False,
                itemstyle_opts={
                    "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                    "emphasis": {
                        "label": {"show": Timeline},
                        "areaColor": "rgba(255,255,255, 0.5)",
                    },
                },
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="" + "全国分地区薪资水平与岗位数量" + str(number),
                    subtitle="",
                    pos_left="center",
                    pos_top="top",
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_size=25, color="rgba(255,255,255, 0.9)"
                    ),
                ),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    formatter=JsCode(
                        """function(params) {
                        if ('value' in params.data) {
                            return params.data.value[2] + ': ' + params.data.value[0];
                        }
                    }"""
                    ),
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_calculable=True,
                    dimension=0,
                    pos_left="30",
                    pos_top="center",
                    range_text=["High", "Low"],
                    range_color=["lightskyblue", "yellow", "orangered"],
                    textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                    min_=min_data,
                    max_=max_data,
                ),
            )
        )

        bar_x_data = [x[0] for x in self.data[number]]
        bar_y_data = [{"name": x[0], "value": x[2]} for x in self.data[number]]
        bar = (
            Bar()
                .add_xaxis(xaxis_data=bar_x_data)
                .add_yaxis(
                series_name="",
                y_axis=bar_y_data,
                label_opts=opts.LabelOpts(
                    is_show=True, position="right", formatter="{b} : {c}"
                ),
            )
                .reversal_axis()
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    max_=self.maxNum, axislabel_opts=opts.LabelOpts(is_show=False)
                ),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(
                    is_calculable=True,
                    dimension=0,
                    pos_left="10",
                    pos_top="top",
                    range_text=["High", "Low"],
                    range_color=["lightskyblue", "yellow", "orangered"],
                    textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                    min_=min_data,
                    max_=max_data,
                ),
            )
        )

        pie_data = [[x[0], x[2]] for x in self.data[number]]
        pie = (
            Pie()
                .add(
                series_name="",
                data_pair=pie_data,
                radius=["15%", "35%"],
                center=["80%", "82%"],
                itemstyle_opts=opts.ItemStyleOpts(
                    border_width=1, border_color="rgba(0,0,0,0.3)"
                ),
            )
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )

        grid_chart = (
            Grid()
                .add(
                bar,
                grid_opts=opts.GridOpts(
                    pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
                ),
            )
                .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
                .add(map_chart, grid_opts=opts.GridOpts())
        )

        return grid_chart

    def refresh(self):
        timeline = Timeline(
            init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
        )
        for y in range(self.count):
            g = self.get_year_chart(y)
            timeline.add(g, time_point=str(y))

        timeline.add_schema(
            orient="vertical",
            is_auto_play=True,
            is_inverse=True,
            play_interval=5000,
            pos_left="null",
            pos_right="5",
            pos_top="20",
            pos_bottom="20",
            width="60",
            label_opts=opts.LabelOpts(is_show=True, color="#fff"),
        )

        timeline.render("全国分地区平均薪资水平及岗位数量.html")
