from functools import reduce

from pymongo import MongoClient
from pyecharts import Bar


class Handle:

    my_set = None

    def __init__(self):
        conn = MongoClient('127.0.0.1', 27017)
        self.my_set = conn.haitou.xuanjiang

    def map_for_place(self, campus):
            return self.my_set.find({"campus":campus}).count()

    def place_pie(self):
        campus_list = ["武汉大学", "华中科技大学", "武汉理工大学", "武汉工程大学", "中国地质大学", "湖北工业大学", "华中农业大学", "华中师范大学", "湖北大学", "长江大学", "武汉科技大学", "中南民族大学", "中南财经政法大学", "三峡大学", "武汉纺织大学", "湖北经济学院", "海投网", "", "江汉大学"]
        count_list = list(map(self.map_for_place, campus_list))
        campus_bar = ["武大", "华科", "理工大", "武工大", "地大", "湖工大", "华农", "华师", "湖大", "长大", "武科大", "民大", "财大", "三峡大", "武纺", "湖经", "其他"]
        count_bar = count_list[:-3] + [(reduce(lambda x, y: x + y, count_list[-3:]))]
        bar = Bar("宣讲会地点分析", "周佳俊 2018-09-27" ,width=1200, height=600)
        bar.add("",campus_bar, count_bar, is_stack=True, is_label_show=True)
        bar.render(path='./dateview/src/places.html')


if __name__ == "__main__":
    handle = Handle()
    handle.place_pie()
