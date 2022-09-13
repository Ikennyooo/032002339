# -*- codeing = utf-8 -*-
# @Time : 2022/9/10 03:10
# @Author : Ikennyooo
# @File : Task2.py
# @Software: PyCharm

import re
import os
import openpyxl as op
import requests
from urllib import request
from bs4 import BeautifulSoup
from pyecharts.charts import Map
from pyecharts.charts import Bar
from pyecharts import options as opts

# 刚开始输入1从第一页爬取。
# 不知为何这个headers不会跳412，如果跳412则调整headers再选择从哪页开始进行爬取（应该不会，全爬了两三次）。
# 多做了境外输入方面的代码，如果有需要可以取出运用。

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
    'Referer': 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml',
    'Cookie': 'yfx_c_g_u_id_10006654=_ck22091015454118598777723981237; sVoELocvxVW0S=5DSg3AJl0Eh2sJMRS0xBrJW.qk641GDuqy0w_08ci5Ki5RdtDaxR5X6SCxJU2lUT2JAIRrk5bgMicvJNmcncBLA; insert_cookie=91349450; _gscu_2059686908=62796040qrs9mc90; _gscbrs_2059686908=1; yfx_f_l_v_t_10006654=f_t_1662795941823__r_t_1662866266927__v_t_1662876292876__r_c_1; security_session_verify=ce983d3c2eeacced2208f3cd4fc9e426; sVoELocvxVW0T=53STdBCWwGhlqqqDkt0rQtG6hvNNyjExrIU3bZflvEnBgUiy0rpSXvPhIFquw.HpHkcLWwzYGQ6eEHopJXmPiqMH7P7nL09.CikMkdGvjHqdEVKzpKiFU60R530mcGomp82jqaQL3a.guQHYmHnb8EGk9nyNGpDJtpIqUlaBaWa4wQtfM3rt96HTunysuql4i5fPS4RFVke8_drqEBZUr9U8w4Ft1xHFp8bgYNqx9XEZOpYCBVMHCFEDNKT2fB88YtHP1XwYLY6rySFRX0sxoeyl3y8i5WhmKypGqBUkoSGuy.tTEACdvFM9IJQglti.iCaRYfu4_EvP28kJ69CTWulvhNH1OSwC6nG1zr6BzkvTG'
}

home_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd{}.shtml'  # 爬取页面主页网址（菜单）。
yearNumber = ''  # 表示年份的全局字符串，在combine函数中进行变更。

localList = []
outSideWuList = []
gatList = []


def get_pic(page_text):
    # 处理数据、获得相应的文本、表格、柱状图、地图展示的函数
    # =======================================================================================================
    # 前置变量的设置
    global localList
    global outSideWuList
    global yearNumber
    global gatList
    title = ''  # 用来存储日期来命名html。
    province = [
        '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西',
        '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西',
        '甘肃', '青海', '北京', '重庆', '上海', '天津', '内蒙古', '广西', '西藏', '新疆', '宁夏',
        '香港', '澳门', '台湾'
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
    # 把爬下来的网页村为txt
    folder = os.path.exists('./文本')
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs('./文本')  # makedirs 创建文件时如果路径不存在会创建这个路径
    txtName = './文本/' + title + '情况.txt'
    with open(txtName, 'a', encoding='utf-8') as txt:
        txt.write(p + '\n')
        txt.close()

    # =======================================================================================================
    # # 每日新增境外输入病例数据的切割
    # pattern = re.compile('。其中境外输入病例.+?例）')  # 利用正则表达式将新增境外输入病例的所需部分提取出来。
    # result = pattern.findall(p)
    # if not result:
    #     pattern = re.compile('均为境外输入病例.+?例）')  # 利用正则表达式对特殊情况进行处理。
    #     result = pattern.findall(p)
    #
    # # 从列表中提取出各个字符串
    # a = ''
    # for i in result:
    #     a = a.join(i)
    #
    # # 制作每日各省份新增境外输入人数的数字形式list
    # outSide = []
    # for i in province:
    #     pattern = re.compile(i + '(?!市)(?!区).+?例')  # 用省份并排除市、区来进行正则匹配。
    #     result = pattern.findall(a)
    #     temp = re.findall("\d+\.?\d*", str(result))  # 将字符串中的数字进行提取。
    #     outSide.append(temp)
    #
    # outSideSee = []  # 用于绘制新增境外输入表格、柱状图、地图的list。
    # for i in outSide:
    #     x = ''.join(list(filter(str.isdigit, str(i))))  # 抽取字符串中的数字（以字符串形式进行存储）。
    #     x = ''.join(x.split())
    #     outSideSee.append(x)

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
                pattern = re.compile('本土病例.+?）。无新')  # 利用正则表达式对特殊情况进行处理。
                result = pattern.findall(p)  # ）；无
                if not result:
                    pattern = re.compile('本土病例.+?）；')  # 利用正则表达式对特殊情况进行处理。
                    result = pattern.findall(p)

    # 从列表中提取出各个字符串
    a = ''
    for i in result:
        a = a.join(i)

    # 制作每日各省份新增本土病例人数的数字形式list
    local = []
    for i in province:
        pattern = re.compile(i + '(?!市)(?!区).+?例')  # 用省份并排除市、区来进行正则匹配。
        result = pattern.findall(a)
        temp = re.findall("\d+\.?\d*", str(result))  # 将字符串中的数字进行提取。
        local.append(temp)

    localSee = []  # 用于绘制新增本土病例表格、柱状图、地图的list。
    for i in local:
        x = ' '.join(list(filter(str.isdigit, str(i))))  # 抽取字符串中的数字（以字符串形式进行存储）。
        x = ''.join(x.split())
        localSee.append(x)

    # ===================================================================================================
    # 新增无症状感染者数据的切割
    pattern = re.compile('.*?新疆生产建设兵团报告新增无症状感染者(.*?)例）。')  # 利用正则表达式将新增无症状感染者的所需部分提取出来。
    result = pattern.findall(p)

    # 从列表中提取出各个字符串
    a = ''
    for i in result:
        a = a.join(i)

    # 制作每日各省份新增无症状感染者人数的数字形式list
    outSideWu = []
    for i in province:
        pattern = re.compile(i + '(?!市)(?!区).+?例')  # 用省份并排除市、区来进行正则匹配。
        result = pattern.findall(a)
        temp = re.findall("\d+\.?\d*", str(result))  # 将字符串中的数字进行提取。
        outSideWu.append(temp)

    outSideWuSee = []  # 用于绘制新增无症状感染者表格、柱状图、地图的list。
    for i in outSideWu:
        x = ''.join(list(filter(str.isdigit, str(i))))  # 抽取字符串中的数字（以字符串形式进行存储）。
        x = ''.join(x.split())
        outSideWuSee.append(x)

    # =======================================================================================================
    # 港澳台病例数据的切割
    pattern = re.compile('累计收到港澳台地区通报确诊病例.+?例）。')  # 利用正则表达式将新增境外输入病例的所需部分提取出来。
    result = pattern.findall(p)
    if not result:
        pattern = re.compile('均为境外输入病例.+?例）')  # 利用正则表达式对特殊情况进行处理。
        result = pattern.findall(p)

    # 从列表中提取出各个字符串。
    a = ''
    for i in result:
        a = a.join(i)

    # 制作港澳台确诊病例人数的数字形式list
    gat = []
    for i in province:
        pattern = re.compile(i + '.+?例')  # 用省份来进行正则匹配
        result = pattern.findall(a)
        temp = re.findall("\d+\.?\d*", str(result))  # 将字符串中的数字进行提取。
        gat.append(temp)

    gatSee = []  # 用于绘制港澳台确诊病例表格、柱状图、地图的list。
    for i in gat:
        x = ''.join(list(filter(str.isdigit, str(i))))  # 抽取字符串中的数字（以字符串形式进行存储）。
        x = ''.join(x.split())
        gatSee.append(x)

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
    # 新增本土病例
    for i in range(0, 34):
        if localSee[i] != '':
            localSee[i] = int(localSee[i])
        # else:
        #     localSee[i] = 0

    # # 新增境外输入
    # for i in range(0, 34):
    #     if outSideSee[i] != '':
    #         outSideSee[i] = int(outSideSee[i])
    #     else:
    #         outSideSee[i] = 0

    # 新增无症状感染者
    for i in range(0, 34):
        if outSideWuSee[i] != '':
            outSideWuSee[i] = int(outSideWuSee[i])
        # else:
        #     localSee[i] = 0

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
    # 柱状图的绘制，运用pyecharts
    # 按照支持的格式对各个list进行格式上的修改
    localBar = []
    outSideWuBar = []
    provinceBar = []
    for i in range(0, 34):
        if localSee[i] or outSideWuSee[i]:
            provinceBar.append(province[i])
            localBar.append(localSee[i])
            outSideWuBar.append(outSideWuSee[i])

    folder = os.path.exists('./柱状图')
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs('./柱状图')  # makedirs 创建文件时如果路径不存在会创建这个路径

    bar = Bar(init_opts=opts.InitOpts(width="1500px", height="800px"))
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

        # 新增境外输入
        # excel.write('新增境外输入\n')
        # excel.write('省份\t人数\n')
        # for i in range(0, 34):
        #     if outSideSee[i]:
        #         excel.write(province[i] + '\t' + str(outSideSee[i]) + '\n')

        # 新增本土病例
        excel.write('新增本土病例\n')
        excel.write('省份\t人数\n')
        for i in range(0, 34):
            if localSee[i]:
                excel.write(province[i] + '\t' + str(localSee[i]) + '\n')
        # 新增无症状感染者
        excel.write('\n新增无症状感染者\n')
        excel.write('省份\t人数\n')
        for i in range(0, 34):
            if outSideWuSee[i]:
                excel.write(province[i] + '\t' + str(outSideWuSee[i]) + '\n')

    # ===================================================================================================
    # 导出为总表格函数
    def get_all_data_excel(name, type_list, in_a_word_list):
        excel_name2 = './表格/总表格/' + name + '情况总表格' + '.xls'
        # 运用openpyxl模块进行表格的绘制
        with open(excel_name2, 'a', encoding='utf-8'):
            wb = op.Workbook()
            ws = wb['Sheet']

            # 对传进来的list进行个性化处理
            typeStr = [title]
            for i in type_list:
                if i == '':
                    typeStr.append('0')
                else:
                    typeStr.append(str(i))
            ws._current_row = 0

            # 对省份list进行个性化处理
            province_for_this = [' ']
            for i in province:
                province_for_this.append(i)
            ws.append(province_for_this)

            # 二者整合后写入
            in_a_word_list.append(typeStr)
            for i in in_a_word_list:
                ws.append(i)
            wb.save(excel_name2)

    # ===================================================================================================
    # 调用上述函数来进行表格的绘制
    folder = os.path.exists('./表格/总表格')
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs('./表格/总表格')  # makedirs 创建文件时如果路径不存在会创建这个路径

    get_all_data_excel('新增本土病例', localSee, localList)
    get_all_data_excel('新增无症状感染者', outSideWuSee, outSideWuList)
    get_all_data_excel('港澳台确诊', gatSee, gatList)

    # ===================================================================================================
    # 将省份与对应数据拼接成['省份','数据']的格式
    localIll = []  # 新增本土病例
    # outSideIll = []  # 新增境外输入
    outSideWuIll = []  # 新增无症状感染者

    for i in range(0, 34):
        eachLocal = [province[i], localSee[i]]
        localIll.append(eachLocal)

    # for i in range(0, 34):
    #     each_outSide = [province[i], outSideSee[i]]
    #     outSideIll.append(each_outSide)

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
    # 发送成功提示
    print(title + '情况' + '处理成功！')
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
    global yearNumber
    home_url = get_html1(home_url)  # 通过方法得到html格式的页面。
    soup = BeautifulSoup(home_url, 'html.parser')
    list_name = soup.select('.list > ul > li > a')
    for item in list_name:
        yearNumber = ''
        for i in range(10, 14):
            yearNumber = yearNumber + item['href'][i]
        yearNumber = yearNumber + '年'
        href = 'http://www.nhc.gov.cn/' + item['href']
        for_each(href)  # 调用for_each对每个网页进行爬取。
        print()


def combine(home_url, page_int):
    # 通过修改参数 '_?' 获得菜单各个页面的网址并传递。
    for i in range(page_int, 41):
        if i == 1:
            url = home_url.format('')
        else:
            url = home_url.format('_' + str(i))
        parse_html(url)


if __name__ == '__main__':
    page_int = int(input('输入你要从哪页开始爬：'))
    combine(home_url, page_int)
