# coding=utf-8
"""
author:cello
"""
import xlwt
import xlrd,json

# 创建一个excel文件

# Worksheets添加sheet
#
# sheet1 = wb.add_sheet('数据')
#
# # Rows and Columns 行与列的表示：
#
# row1 = sheet1.row(1)
# col0 = sheet1.col(0)
#
# # cells值
#
# sheet1.write(0,1,'B1')
# row1.write(0,'A2')

# data = xlrd.open_workbook('douyu.xls')
wb = xlwt.Workbook('douyu.xls')
sheets = wb.add_sheet('数据')
with open('move.json','r') as jsonfile:
    move_dict = jsonfile.read()

move_list= move_dict.split(',\n')
print(move_list[-1])
print(type(move_list))
print(eval(move_list[0]))
for index,i in enumerate(eval(move_list[0])):
    sheets.write(0,index,i)

try:
    for index,data1 in enumerate(move_list):
        print(data1)
        data = eval(data1)
        print(data)
        sheets.write(index+1,0,data['url'])
        sheets.write(index + 1, 1,data['name'])
except Exception as f:
    print(f)
    pass

wb.save('douyu.xls')

