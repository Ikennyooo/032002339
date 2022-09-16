import xlrd

book = xlrd.open_workbook('./表格/总表格/新增本土病例情况总表格.xls')
sheet1 = book.sheets()[0]

for i in range(1, 35):
    flag = 0
    index = -1
    col_i_values = sheet1.col_values(i)
    for j in col_i_values:
        index = index + 1
        if index == 0:
            continue
        if int(j) >= 100:
            flag = flag + 1
            output = ''.join(sheet1.col_values(i)[0] + sheet1.row_values(index)[0] + '新增' + str(j) + '例\n')
            with open('./表格/总表格/新增本土病例热点分析.txt', 'a', encoding='utf-8') as f:
                f.write(output)
            if index + 1 == sheet1.nrows:
                if flag >= 6:
                    with open('./表格/总表格/新增本土病例热点分析.txt', 'a', encoding='utf-8') as f:
                        f.write('🔺🔺🔺' + sheet1.col_values(i)[0] + '近阶段疫情严重，持续' + str(flag) + '天🔺🔺🔺\n')
                if flag > 0:
                    with open('./表格/总表格/新增本土病例热点分析.txt', 'a', encoding='utf-8') as f:
                        f.write('==============================================\n')
                flag = 0

        elif int(j) < 100:
            if flag >= 6:
                with open('./表格/总表格/新增本土病例热点分析.txt', 'a', encoding='utf-8') as f:
                    f.write('🔺🔺🔺' + sheet1.col_values(i)[0] + '近阶段疫情严重，持续' + str(flag) + '天🔺🔺🔺\n')
            if flag > 0:
                with open('./表格/总表格/新增本土病例热点分析.txt', 'a', encoding='utf-8') as f:
                    f.write('==============================================\n')
            flag = 0
# book = xlrd.open_workbook('./表格/总表格/新增本土病例情况总表格.xls')
# sheet1 = book.sheets()[0]
# nrows = sheet1.nrows
# print('表格总行数', nrows)
# ncols = sheet1.ncols
# print('表格总列数', ncols)
# row3_values = sheet1.row_values(2)
# print('第3行值', row3_values)
# col3_values = sheet1.col_values(2)
# print('第3列值', col3_values)
# cell_3_3 = sheet1.cell(2, 2).value
# print('第3行第3列的单元格的值：', cell_3_3)
