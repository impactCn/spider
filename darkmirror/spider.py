from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

base_url = "https://weixin.sogou.com/weixin?"
conten_base_url = "https://weixin.sogou.com"
keyword = "辟谷"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "ABTEST=2|1533602887|v1; IPLOC=CN3301; SUID=6211A07C771A910A000000005B68EC47; SUID=6211A07C2013940A000000005B68EC47; weixinIndexVisited=1; Hm_lvt_e60c55838acbc89c7409eced091b4723=1533602888; SUV=00574F766544571A5B68EC479A331927; sct=1; SNUID=6112A478030676C9C2BFD56B041C3378; JSESSIONID=aaaS3WIPkbZAJ6EjT76tw; ppinf=5|1533602986|1534812586|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMDpIdW5rJTIwU3VufGNydDoxMDoxNTMzNjAyOTg2fHJlZm5pY2s6MTA6SHVuayUyMFN1bnx1c2VyaWQ6NDQ6bzl0Mmx1TV9sdnNTemswWGdpSkNndTdFeHdYc0B3ZWl4aW4uc29odS5jb218; pprdig=TIQegdMe3omtNzq6RLk9fvEllgOLSpAwWcHpkKfT9UQ8E61cFdrjVwO5Cwcg7FE6o83CSSizwcmbYrdO_2EmImjw7v6j4taNJbQwFKSHNa7bOJp0wYwNM5fuleU7QhYL1KrhcGRCeYqh4e1qcZdz4ZUPH8Rfe4BkmtSTNFmPWc4; sgid=04-34361629-AVto7KoO0ZOxp6oNrjukvIs; ppmdig=153360298700000057744d66c29a2d7e98534e85970ed4d9; Hm_lpvt_e60c55838acbc89c7409eced091b4723=1533605859",
    "Host": "weixin.sogou.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/5"
                  "37.36"
}
# proxy_pool_url = "http://127.0.0.1:5555/random"
max_count = 5
MONGO_URL = 'localhost'
MONGO_DB = 'weixin'
MONGO_CONNECTION = 'articles'



# def get_proxy():
#     try:
#         response = requests.get(proxy_pool_url)
#         if response.status_code == 200:
#             return response.text
#         return None
#     except ConnectionError:
#         return None


def get_html(url, count=1):
    print("Crawling", url)
    print("Trying Count", count)
    # proxy = get_proxy()
    # print("Using Proxy", proxy)
    if count >= max_count:
        print("Tried Too Many Counts")
        return None
    try:
        # proxies = {
        #     'http': 'http://' + proxy
        # }
        response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            print("200")
            return response.text
        if response.status_code == 302:
            print("302")
            # proxy = get_proxy()
            # if proxy:
            #     print('Using Proxy', proxy)
            #     return get_html(url)
            # else:
            #     print("Get Proxy Failed")
            #     return None
        else:
            print(555)
            return None
    except ConnectionError as e:
        print("Error Qccurred", e.args)
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'type': 2,
        'query': keyword,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        print(conten_base_url + item.attr('href'))
        yield conten_base_url + item.attr('href')


def get_detail(url):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:

            print(response.text)
            article_url = response.text.split('url += \'')[1].replace("';", "")
            ar_response = requests.get(article_url, headers)
            return ar_response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text().strip()
    content = doc('.rich_media_content').text().replace(r'\n', '')
    date = doc('#publish_time').text().strip()
    nickname = doc('#js_name').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    return {
        'title': title,
        'content': content,
        'date': date,
        'nickname': nickname,
        'wechat': wechat
    }


# def save_to_mongo(data):
#     if db[MONGO_CONNECTION].update({'title': data['title']}, {'$set': data}, True):
#         print("保存到MongoDB成功", data['title'])
#     else:
#         print("保存到MongoDB失败", data['title'])


def main():
    for page in range(1, 10):
        html = get_index(keyword, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)


if __name__ == '__main__':
    main()
