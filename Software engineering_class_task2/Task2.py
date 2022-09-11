# -*- codeing = utf-8 -*-
# @Time : 2022/9/10 03:10
# @Author : Ikennyooo
# @File : inaWordMine.py
# @Software: PyCharm

import re
import os
import requests
from urllib import request
from bs4 import BeautifulSoup
from pyecharts.charts import Map
from pyecharts.charts import Bar
from pyecharts import options as opts

# 【重要事项】声明请求的相关属性。在要进行爬取时需更新headers中的cookie方可进行爬取，不然会报错412。
# 如中途出现412中断，可更改cookie后，调整combine函数中的页码数进行继续爬。

cookie = input('New cookie: ')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
    'Cookie': cookie
}
home_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd{}.shtml'  # 爬取页面主页网址（菜单）。
yearNumber = ''  # 表示年份的全局字符串，在combine函数中进行变更。


def get_pic(page_text):
    # 处理数据，获得相应的地图展示。可跳转至248行查看爬虫的编写。
    # =======================================================================================================
    # 前置变量的设置
    global yearNumber
    title = ''  # 用来存储日期来命名html。
    province = [
        '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西',
        '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西',
        '甘肃', '青海', '台湾', '北京', '重庆', '上海', '天津',
        '内蒙古', '广西', '西藏', '新疆', '宁夏', '香港', '澳门', '台湾'
    ]  # 各个省份province。

    # =======================================================================================================
    # 将文本运用美丽汤的select函数切割出来
    soup2 = BeautifulSoup(page_text, 'lxml')
    px = soup2.select('p')
    p = ''
    for i in px:
        py = ''.join(i.text)
        p = p + py  # 将每段进行拼接。

    # =======================================================================================================
    # 将日期切割出来用于文件名的编写
    pattern = re.compile('.+日0—24时')  # 利用正则表达式将新增境外输入病例的所需部分提取出来。
    result = pattern.findall(p)
    for i in result:
        title = ''.join(i)
    title = yearNumber + title

    # =======================================================================================================
    # 每日新增境外输入病例数据的切割
    pattern = re.compile('。其中境外输入病例.+?例）')  # 利用正则表达式将新增境外输入病例的所需部分提取出来。
    result = pattern.findall(p)
    if not result:
        pattern = re.compile('均为境外输入病例.+?例）')  # 利用正则表达式对特殊情况进行处理。
        result = pattern.findall(p)

    a = ''  # 从列表中提取出各个字符串。
    for i in result:
        a = a.join(i)

    outSide = []

    for i in province:
        pattern = re.compile(i + '.+?例')  # 用省份来进行正则匹配
        result = pattern.findall(a)
        temp = re.findall("\d+\.?\d*", str(result))  # 将字符串中的数字进行提取。
        outSide.append(temp)

    outSideSee = []  # 境外输入绘制的list。

    for i in outSide:
        x = ''.join(list(filter(str.isdigit, str(i))))
        x = ''.join(x.split())
        outSideSee.append(x)

    # ===================================================================================================
    # 每日新增本土病例病例数据的切割
    pattern = re.compile('本土病例.+?），含')  # 利用正则表达式将新增本土病例的所需部分提取出来。
    result = pattern.findall(p)
    if not result:
        pattern = re.compile('本土病例.+?），含')  # 利用正则表达式对特殊情况进行处理。
        result = pattern.findall(p)
        if not result:
            pattern = re.compile('本土病例.+?）；无')  # 利用正则表达式对特殊情况进行处理。
            result = pattern.findall(p)  # ）；无
            if not result:
                pattern = re.compile('本土病例.+?）；')  # 利用正则表达式对特殊情况进行处理。
                result = pattern.findall(p)

    a = ''  # 从列表中提取出各个字符串。
    for i in result:
        a = a.join(i)

    local = []

    for i in province:
        pattern = re.compile(i + '.+?例')  # 用省份来进行正则匹配
        result = pattern.findall(a)
        temp = re.findall("\d+\.?\d*", str(result))  # 将字符串中的数字进行提取。
        local.append(temp)

    localSee = []  # 境外输入绘制的list。

    for i in local:
        x = ' '.join(list(filter(str.isdigit, str(i))))
        x = ''.join(x.split())
        localSee.append(x)

    # ===================================================================================================
    # 新增无症状感染者数据的切割
    pattern = re.compile('.*?新疆生产建设兵团报告新增无症状感染者(.*?)例）。')  # 利用正则表达式将新增无症状感染者的所需部分提取出来。
    result = pattern.findall(p)

    a = ''  # 从列表中提取出各个字符串。
    for i in result:
        a = a.join(i)

    outSideWu = []

    for i in province:
        pattern = re.compile(i + '.+?例')  # 用省份来进行正则匹配
        result = pattern.findall(a)
        temp = re.findall("\d+\.?\d*", str(result))  # 将字符串中的数字进行提取。
        outSideWu.append(temp)

    outSideWuSee = []  # 境外输入绘制的list

    for i in outSideWu:
        x = ''.join(list(filter(str.isdigit, str(i))))
        x = ''.join(x.split())
        outSideWuSee.append(x)

    # ===================================================================================================
    # 如果用jieba来切割文本，可以将此处代码取出调试。
    # f = open('txtForEach1.txt', 'r', encoding='utf-8')
    # t = f.read()
    # f.close()
    # cut = []
    # ls = jieba.lcut(t)
    # cut.append(ls)
    # txt = " ".join(ls)
    # print(cut)
    # print(txt)

    # ===================================================================================================
    # 将各个list中的数据转换为数字
    for i in range(0, 34):
        if localSee[i] != '':
            localSee[i] = int(localSee[i])
        # else:
        # localSee[i] = 0

    for i in range(0, 34):
        if outSideSee[i] != '':
            outSideSee[i] = int(outSideSee[i])
        # else:
        # outSideSee[i] = 0

    for i in range(0, 34):
        if outSideWuSee[i] != '':
            outSideWuSee[i] = int(outSideWuSee[i])
        # else:
        # localSee[i] = 0

    # ===================================================================================================
    # 用于检验的输出
    print('这是province（省份）')
    print(province)
    # print('这是outSideSee（新增境外输入）')
    # print(outSideSee)
    print('这是localSee（新增本土病例）')
    print(localSee)
    print('这是outSideWuSee（新增无症状感染者）')
    print(outSideWuSee)

    # ===================================================================================================
    # 此处本来想画一个柱状图，后来想一想用地图比较好表示。如果要更改为柱状图可将此处代码取出修改。

    localBar = []
    outSideWuBar = []
    provinceBar = []
    for i in range(0, 34):
        if localSee[i] or outSideWuSee[i]:
            provinceBar.append(province[i])
            localBar.append(localSee[i])
            outSideWuBar.append(outSideWuSee)

    folder = os.path.exists('./柱状图')
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs('./柱状图')  # makedirs 创建文件时如果路径不存在会创建这个路径

    bar = Bar(init_opts=opts.InitOpts(width="2500px", height="1000px"))
    bar.add_xaxis(provinceBar)
    bar.add_yaxis('新增本土', localBar)
    bar.add_yaxis('新增无症状', outSideWuBar)
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title + '本土病例'))
    html = './柱状图/' + title + '情况柱状图' + '.html'
    bar.render(html)

    # ===================================================================================================
    # 导出为excel表格
    folder = os.path.exists('./表格')
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs('./表格')  # makedirs 创建文件时如果路径不存在会创建这个路径

    excel_name = './表格/' + title + '情况表格' + '.xls'
    with open(excel_name, 'w', encoding='utf-8') as excel:
        excel.write(title + '相关情况\n')

        # excel.write('新增境外输入\n')
        # excel.write('省份\t人数\n')
        # for i in range(0, 34):
        #     if outSideSee[i]:
        #         excel.write(province[i] + '\t' + str(outSideSee[i]) + '\n')

        excel.write('新增本土病例\n')
        excel.write('省份\t人数\n')
        for i in range(0, 34):
            if localSee[i]:
                excel.write(province[i] + '\t' + str(localSee[i]) + '\n')
        excel.write('\n新增无症状感染者\n')
        excel.write('省份\t人数\n')
        for i in range(0, 34):
            if outSideWuSee[i]:
                excel.write(province[i] + '\t' + str(outSideWuSee[i]) + '\n')

    # ===================================================================================================
    # 将省份与对应数据拼接成['省份','数据']的格式
    localIll = []  # 新增本土病例
    outSideIll = []  # 新增境外输入
    outSideWuIll = []  # 新增无症状感染者

    for i in range(0, 34):
        eachLocal = [province[i], localSee[i]]
        localIll.append(eachLocal)

    for i in range(0, 34):
        each_outSide = [province[i], outSideSee[i]]
        outSideIll.append(each_outSide)

    for i in range(0, 34):
        each_outSideWu = [province[i], outSideWuSee[i]]
        outSideWuIll.append(each_outSideWu)

    # ===================================================================================================
    # 导出为带数据地图的html文件
    folder = os.path.exists('./地图')
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs('./地图')  # makedirs 创建文件时如果路径不存在会创建这个路径

    def create_china_map():
        mapName = './地图/' + title + '情况' + '.html'  # 文件名格式：'某年某月某日0-24时情况.html'。
        (
            Map(init_opts=opts.InitOpts(width="2000px", height="1000px", page_title="ik软工第二次作业"))
                .add(
                series_name='本土',
                data_pair=localIll,
                maptype="china",
            )
                #     .add(
                #     series_name='境外',
                #     data_pair=outSideIll,
                #     maptype="china",
                # )
                .add(
                series_name='无症状',
                data_pair=outSideWuIll,
                maptype="china",
            )
                .set_global_opts(title_opts=opts.TitleOpts(title=title + '情况'))
                .render(mapName)
        )

    create_china_map()

    # ===================================================================================================
    # 检验输出
    print(title)
    print('新增本土病例:')
    print(localIll)
    # print('新增境外输入：')
    # print(outSideIll)
    print('新增无症状感染者：')
    print(outSideWuIll)

    # ===================================================================================================


def for_each(url):
    # 进行网页的爬取，将text格式页面传给get_pic进行地图绘制
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    get_pic(page_text)


def get_html1(home_url):
    # 得到html格式页面的函数，并将html返回（用于parse_html）。
    req = request.Request(url=home_url, headers=headers)
    html = request.urlopen(req).read().decode('utf-8')
    return html


def parse_html(home_url):
    # 调用请求函数，获取一级页面
    home_url = get_html1(home_url)  # 通过方法得到html格式的页面。
    soup = BeautifulSoup(home_url, 'html.parser')
    list_name = soup.select('.list > ul > li > a')
    for item in list_name:
        href = 'http://www.nhc.gov.cn/' + item['href']
        for_each(href)  # 调用for_each对每个网页进行爬取。
        print()


def combine(home_url):
    # 通过修改参数 '_?' 获得菜单各个页面的网址并传递。
    global yearNumber
    for i in range(1,11):
        if i == 1:
            url = home_url.format('')
        else:
            url = home_url.format('_' + str(i))
        yearNumber = '2022年'  # 2022年数据的抓取。
        parse_html(url)

    # for i in range(12, 25):
    #     if i == 1:
    #         url = home_url.format('')
    #     else:
    #         url = home_url.format('_' + str(i))
    #     yearNumber = '2021年'  # 2021年数据的抓取。
    #     parse_html(url)
    #
    # for i in range(27, 41):
    #     if i == 1:
    #         url = home_url.format('')
    #     else:
    #         url = home_url.format('_' + str(i))
    #     yearNumber = '2020年'  # 2020年数据的抓取。
    #     parse_html(url)


if __name__ == '__main__':
    combine(home_url)
