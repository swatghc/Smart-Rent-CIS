import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


# 用来爬取realestate信息
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 从返回的页面数据中用正则表达式提取所需信息
def parse_one_page(html):

    # re.S 表示可以匹配任意的字符
    pattern = re.compile('data-featured-status.*?<a href="(.*?)" >' +
                         '.*?agent-photo" src="(.*?)"' +
                         '.*?title="(.*?)"' +
                         '.*?priceText">(.*?)<' +
                         '.*?listingName.>(.*?)<' +
                         '.*?Bedrooms</span></dt> <dd>(\d+)<' +
                         '.*?Bathrooms</span></dt> <dd>(\d+)<', re.S)
    items = re.findall(pattern, html)

    # 格式化，变成字典
    for item in items:
        yield {
            'urlDetail': 'https://www.realestate.com.au' + item[0],
            'agentPic': item[1],
            'agent': item[2],
            'price': item[3],
            'location': item[4],
            'bed': item[5],
            'bathroom': item[6]
        }


# 写入文档
# encoding = 'utf-8'
# ensure_ascii = False
# 确保写入的是中文而不是ascii码
def write_to_file(content):
    with open('result.txt', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')
        f.close()


def main(list):
    url = 'https://www.realestate.com.au/rent/in-melbourne,+vic/list-' + str(list)
    html = get_one_page(url)
    print(html)
    for item in parse_one_page(html):
        write_to_file(item)
        return item

# 单进程，速度慢
# if __name__ == '__main__':
#     for i in range(100):
#         main(i)

# 多进程，提升速度
if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(1)])