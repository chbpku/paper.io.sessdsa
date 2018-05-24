import requests, re


def grab_code(filename):
    url = 'https://raw.githubusercontent.com/chbpku/paper.io.sessdsa/master/%s' % filename
    print('下载 %s ...' % url, end='', flush=True)
    web_raw = requests.get(url)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(web_raw.text.replace('\r\n', '\n'))
    print('完成')


print('连接github仓库...', end='', flush=True)
main = requests.get('https://github.com/chbpku/paper.io.sessdsa')
items = re.findall(r'href="/chbpku/paper.io.sessdsa/blob/master/(.+?)"',
                   main.text)
print('完成')
codes = [i for i in items if i.endswith('.md') or i.endswith('.py')]
print('获取到%d个代码文件：%s' % (len(codes), ', '.join(codes)))
for code in codes:
    grab_code(code)