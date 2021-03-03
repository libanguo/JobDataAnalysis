import pymongo
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation


class MyGif:
    def __init__(self, frequency):
        self.frequency = frequency  # 设置刷新频率
        self.dataframe = []
        self.count = 0  # 自增，每次add_data后加一
        self.max_data_size = 50  # 避免保存的数据组过大导致动画渲染时间变长

        # 用plt加理图表，figsize表示图标长宽，ax表示标签
        self.fig, self.ax = plt.subplots(figsize=(15, 8))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

    def add_edu_data(self, new_item):  # new_item为二维数组
        self.dataframe.append(new_item)
        self.count = self.count + 1
        if len(self.dataframe) > self.max_data_size:
            self.dataframe.remove[self.dataframe[0]]
        if self.count % self.frequency == 0:
            self.generate_edu_animation()

    def generate_edu_animation(self):  # 此运行方法需要先安装ffmpeg
        animator = animation.FuncAnimation(self.fig, self.get_edu_salary_barchart, frames=self.count)
        animator.save("动态排序-学历.gif")

    def get_edu_salary_barchart(self, number):  # 此方法绘制学历-平均薪资条形图
        edu_color = {'不限': "#90d295", '大专': "#f7b15f", '本科': "#eaf450", '硕士': "#adb4ff", '博士': "#abc123"}
        edu_salary_list = self.dataframe[number - 1]
        edu = [x[0] for x in edu_salary_list]
        average_salary = [x[1] for x in edu_salary_list]
        # 所有坐标、标签清除
        self.ax.clear()
        # 显示颜色、学历名字
        self.ax.barh(edu, average_salary, color=[edu_color[e] for e in edu])

        dx = max(average_salary) / 20

        # ax.text(x,y,name,font,va,ha)
        # x,y表示位置；
        # name表示显示文本；
        # va,ba分别表示水平位置，垂直放置位置；
        for i, (value, name) in enumerate(zip(average_salary, edu)):
            self.ax.text(value - dx, i, name, size=14, weight=600, ha='right', va='center')
            self.ax.text(value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center')

        # ax.transAxes表示轴坐标系，(1,0.4)表示放置位置
        self.ax.text(0, 1.06, 'Average Salary', transform=self.ax.transAxes, size=12, color='#777777')

        # set_major_formatter表示刻度尺格式；
        self.ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        self.ax.xaxis.set_ticks_position('top')
        self.ax.tick_params(axis='x', colors='#777777', labelsize=12)
        self.ax.set_yticks([])
        # margins表示自动缩放余额；
        self.ax.margins(0, 0.01)
        # 设置后面的网格
        self.ax.grid(which='major', axis='x', linestyle='-')
        # 刻度线和网格线是在图标上方还是下方，True为下方
        self.ax.set_axisbelow(True)
        self.ax.text(0, 1.15, '各学历平均薪资',
                     transform=self.ax.transAxes, size=24, weight=600, ha='left', va='top')
        self.ax.text(1, 0, 'by@Jsx', transform=self.ax.transAxes, color='#777777', ha='right',
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
        # 取消图表周围的方框显示
        plt.box(False)
