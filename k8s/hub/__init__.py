# coding:utf8
import requests

# from pyquery import PyQuery as pq

#  封装请求头部
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
}
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 生成随机的heards，网站有反爬虫的可能。
# def get_image_header():
#     return {'User-Agent': random.choice(UserAgent_List),
#             'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#             'Cache-Control': 'no-cache',
#             'Upgrade-Insecure-Requests': '1',
#     }


urls_project = 'http://hub.cbble.com/api/projects'
url_repo = 'http://hub.cbbnle.com/api/repositories?project_id='
url_hub = 'http://hub.cbbnle.com/'


def login():
    s = requests.Session()  # 可以在多次访问中保留cookie
    s.post('http://hub.cbble.com/login', {'principal': 'admin', 'password': 'Fs9006'},
           headers=headers)  # POST帐号和密码，设置headers
    return s


# 由于现在只用一个项目有, 直接写死, 暂不不调用该方法
def get_project(url='http://hub.cbble.com/api/projects'):
    s = login()
    ret = s.get(url)  # 已经是登录状态了
    dit = ret.json()
    d = {}
    for i in dit:
        # d.setdefault(i.get('name'), []).append(i.get('project_id'))
        d.setdefault(i.get('project_id'), i.get('name'))
    return d


def get_project_id(repo):
    project = get_project()
    print(project)
    for k, v in project.items():
        if v == repo:
            return k


# print(get_project())

# for i in get_project():
#     print(i)


def get_tags(repo_name, urls='http://hub.cbble.com/api'):
    url = urls + '/repositories/%s/tags' % repo_name
    s = login()
    tags = s.get(url)
    tmp = []
    for i in tags.json():
        tmp.append(i.get('name'))
    return tmp[-3:]


def get_image_name(url='http://hub.cbble.com/api/repositories?project_id=', project_id=11):
    s = login()
    urls = url + str(project_id)
    ret = s.get(urls)
    tmp = []
    for i in ret.json():
        tmp.append(i.get('name'))

    return tmp


def get_all():
    ret = dict()
    image_list = dict()
    project = get_project()
    for i, j in project.items():
        image = get_image_name(project_id=i)
        for k in image:
            image_list[k] = get_tags(k)
        ret[j] = image_list
    return ret


if __name__ == '__main__':
    # a = get_tags('test/pro-hsd-approve-web')
    # print(a)
    # print(get_project())
    print(get_project())
    # print(get_image_name(project_id=6))
    print(get_project_id("rule"))
