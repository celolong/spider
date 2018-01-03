#coding:utf-8
import requests
import re
from lxml import etree



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}

# start_url = 'https://www.tianyancha.com/login'
# start_url = 'https://www.tianyancha.com/company/3053356683'
start_url = 'https://www.tianyancha.com/company/1198318187'
# start_url = 'https://www.tianyancha.com/company/9519792'


# 构建cookies
temp = 'TYCID=3df92250d8e411e7a3d1a380901d7a2f; undefined=3df92250d8e411e7a3d1a380901d7a2f; ssuid=4135465791; RTYCID=aa55d6044379426fb784a667ef172d63; aliyungf_tc=AQAAALFJmE+UzwEA3lnptw1hApEs3ntf; csrfToken=iv7XNOageB2IzJpl2EHvp-2s; jsid=SEM-BAIDU-PZPC-000000; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODg5NTczNDU2NiIsImlhdCI6MTUxMjQ1MDQ3MywiZXhwIjoxNTI4MDAyNDczfQ.GeAWDotDcJNrTyWTP-hkHUn9GoEulv-UvNzNO-JFf5H85lj7371bI2HjYfOdLxTFFgbZBobW5QfrT9j_dxNSZQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218895734566%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODg5NTczNDU2NiIsImlhdCI6MTUxMjQ1MDQ3MywiZXhwIjoxNTI4MDAyNDczfQ.GeAWDotDcJNrTyWTP-hkHUn9GoEulv-UvNzNO-JFf5H85lj7371bI2HjYfOdLxTFFgbZBobW5QfrT9j_dxNSZQ; _csrf=Mf9X8sSPUabIfBIwNK1qpg==; OA=NdQHLGMAaiTowD4Mj5b7jrJiBC02YfHgt/kkxqOs3uk=; _csrf_bk=c1aef85900ace405ea4fdc3d89554b58; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1512445332,1512445371,1512445816,1512448027; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1512450473'
cookies = {}
for i in temp.split('; '):
    cookies[i.split('=')[0]] = i.split('=')[1]
# print(cookies)     打印之后为字典格式，如下↓
# cookies = {
#     'TYCID':'40c68e40d8a411e7a643575d241e5aaa',
#     'undefined':'40c68e40d8a411e7a643575d241e5aaa',
#     'ssuid':'735211370',
#     'RTYCID':'37058f86adbf4382a4cbb5de84b8cb43',
#     'aliyungf_tc':'AQAAACdgfD4/FgEARkDttyxvXuZxzMU1',
#     'csrfToken':'Q7maGZgsAOJ93vWCmzODYby7',
#     'tyc-user-info':'%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTY3OTc5MDEzMCIsImlhdCI6MTUxMjQzNjc2NywiZXhwIjoxNTI3OTg4NzY3fQ.qK0wK0R-8YPmsz9K-uztbwm6B2aKkcM-8vw0VtplLetZ2bHYFyf1RN_Spsg07qJvLwq0LpfCTgf0zef8rC2jdQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215679790130%2522%257D',
#     'auth_token':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTY3OTc5MDEzMCIsImlhdCI6MTUxMjQzNjc2NywiZXhwIjoxNTI3OTg4NzY3fQ.qK0wK0R-8YPmsz9K-uztbwm6B2aKkcM-8vw0VtplLetZ2bHYFyf1RN_Spsg07qJvLwq0LpfCTgf0zef8rC2jdQ',
#     'bannerFlag':'true',
#     'jsid':'SEM-BAIDU-PZPC-000000',
#     '_csrf':'cPmIxfsL9w5S1A5XvcDruw==',
#     'OA':'zpVuhLQZtH+e61XYk45Pka1iPuT1OiDsqBGUxVvBR9AXumnHz1ptCpsvvgTy27Q4',
#     '_csrf_bk':'cf5fc0976ac8e6521b65b2bbdd41663a',
#     'Hm_lvt_e92c8d65d92d534b0fc290df538b4758':'1512373258,1512393795,1512436749,1512445414',
#     'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758':'1512455905'
# }



# 使用 requests 发送 get 请求，获取响应信息
response = requests.get(start_url, headers=headers, cookies=cookies)
# response.content得到页面的数据，.decode()将页面数据转换成string格式
data = response.content.decode()


# 保存网页。
# with open('tianyan.html', 'w') as f:
#     f.write(data)


# 定义爬取数据的正则表达式
re_name = re.compile('<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>', re.S)
re_tel = re.compile('<span class="sec-c3">电话：</span><span>(.*?)</span>', re.S)
re_email = re.compile('emailWidth">(.*?)</span>')
# 利用正则表达式查找到数据
company_name = re_name.findall(data)
print(company_name)

def find(rule):
    return rule.findall(data)

company_tel = find(re_tel)
c_email = find(re_email)

print(company_tel)
print(c_email)




# 上面利用正则和下面利用 xpath 获取的数据都是一个列表。因为有些内容是空的，所以使用list[0]获取数据会报错




# xpath：利用etree.HTML，将html字符串转化为Element对象
html = etree.HTML(data)

# Element对象具有xpath的方法，利用xpath寻找到数据
url_list = html.xpath('//div[@class="f14 sec-c2"]/div[1]/a/text()')
desc_list = html.xpath('//*[@id="company_base_info_detail"]/text()')
ceo_list = html.xpath('//div[@class="company-human-box position-rel in-block vertical-top text-left float-left point"]/div[1]/div[2]/div/a/text()')
money_list = html.xpath('//div[@class="new-border-bottom"]/div[2]/div/text/text()')
scope_list = html.xpath('//table[@class="table companyInfo-table f14"]/tbody/tr[7]/td[2]/span/span/span[1]/text()')


print(url_list)
print(desc_list)
print(ceo_list)
print(money_list)
print(scope_list)

